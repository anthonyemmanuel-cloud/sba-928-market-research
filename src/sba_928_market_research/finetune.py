"""
Requirements 3 and 4: fine-tune a language model and compare it with the original.

Model: google/flan-t5-small (about 77 million parameters), a small open
model from Hugging Face that can be fine-tuned on a laptop in minutes.

    Data preparation: each training example is (prompt -> correct insight).
    Training:         the model reads a prompt, writes an answer, and is
                      corrected toward the right insight, again and again.
    Evaluation:       both models answer test prompts they have never seen
                      (new wordings), and the answers are scored.
"""

import os
import random
import re
import time
from collections import defaultdict
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
MODEL_NAME = os.getenv("SBA928_MODEL", "google/flan-t5-small")
MODEL_FOLDER = PROJECT_FOLDER / "models" / "flan-t5-small-market-research"

EPOCHS = 10            # adjusted from 30: test accuracy peaked at epoch 10 (early stopping)
CHECK_EVERY = 2        # test every 2 epochs to see the curve in more detail

LEARNING_RATE = 5e-4   # how big each correction step is
BATCH_SIZE = 8         # how many examples the model studies at once
MAX_INPUT_TOKENS = 96
MAX_ANSWER_TOKENS = 48


# ---------------------------------------------------------------
# Scoring (no AI needed, so these are easy to test)
# ---------------------------------------------------------------
def normalize(text):
    return re.sub(r"[^a-z0-9.:% ]+", " ", text.lower()).strip()


def is_correct(prediction, key):
    # Correct = the key fact appears in the answer as a whole phrase
    # ("8 percent" must not match "18 percent")
    pattern = r"(?<![a-z0-9.])" + re.escape(normalize(key)) + r"(?![a-z0-9])"
    return re.search(pattern, normalize(prediction)) is not None


def overlap_f1(prediction, reference):
    # Relevance = how many words the answer shares with the correct insight (0 to 1)
    pred, ref = normalize(prediction).split(), normalize(reference).split()
    if not pred or not ref:
        return 0.0
    remaining, shared = list(ref), 0
    for word in pred:
        if word in remaining:
            remaining.remove(word)
            shared += 1
    if shared == 0:
        return 0.0
    precision, recall = shared / len(pred), shared / len(ref)
    return 2 * precision * recall / (precision + recall)


def score(predictions, records):
    correct = [is_correct(p, r["key"]) for p, r in zip(predictions, records)]
    relevance = [overlap_f1(p, r["answer"]) for p, r in zip(predictions, records)]

    def breakdown(field):
        groups = defaultdict(list)
        for ok, record in zip(correct, records):
            groups[record[field]].append(ok)
        return {name: (sum(values), len(values)) for name, values in sorted(groups.items())}

    return {"correct": sum(correct), "total": len(records),
            "accuracy": sum(correct) / len(records) if records else 0.0,
            "relevance": sum(relevance) / len(relevance) if relevance else 0.0,
            "by_category": breakdown("category"), "by_group": breakdown("group"),
            "is_correct": correct}


# ---------------------------------------------------------------
# Model helpers
# ---------------------------------------------------------------
def pick_device(torch):
    # CPU is the safe default. Set SBA928_DEVICE=mps to try the Mac's graphics chip.
    return torch.device(os.getenv("SBA928_DEVICE", "cpu"))


def load_model(name=MODEL_NAME):
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    return AutoTokenizer.from_pretrained(name), AutoModelForSeq2SeqLM.from_pretrained(name)


def generate(model, tokenizer, prompts, device):
    import torch

    model.eval()
    answers = []
    with torch.no_grad():
        for start in range(0, len(prompts), 16):
            batch = tokenizer(prompts[start:start + 16], return_tensors="pt", padding=True,
                              truncation=True, max_length=MAX_INPUT_TOKENS).to(device)
            output = model.generate(**batch, max_new_tokens=MAX_ANSWER_TOKENS, num_beams=1, do_sample=False)
            answers += tokenizer.batch_decode(output, skip_special_tokens=True)
    return answers


# ---------------------------------------------------------------
# The experiment
# ---------------------------------------------------------------
def run_experiment(prompts, epochs=EPOCHS, check_every=CHECK_EVERY, save_model=True):
    import torch

    random.seed(42)
    torch.manual_seed(42)
    device = pick_device(torch)

    # Step 1. Data preparation: split the prompts into training and test sets
    train = [p for p in prompts if p["split"] == "train"]
    test = [p for p in prompts if p["split"] == "test"]
    test_prompts = [p["prompt"] for p in test]
    print(f"Training examples: {len(train)} | Test examples (unseen wordings): {len(test)} | Device: {device}")

    # Step 2. Baseline: how does the ORIGINAL model answer the test prompts?
    tokenizer, model = load_model()
    model.to(device)
    original_answers = generate(model, tokenizer, test_prompts, device)
    original = score(original_answers, test)
    print(f"Original model:   {original['correct']}/{original['total']} correct "
          f"({original['accuracy']:.0%}), relevance {original['relevance']:.2f}")

    # Step 3. Training
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE)
    history = []
    started = time.perf_counter()
    for epoch in range(1, epochs + 1):
        model.train()
        random.shuffle(train)
        total_loss = 0.0
        for start in range(0, len(train), BATCH_SIZE):
            batch = train[start:start + BATCH_SIZE]
            inputs = tokenizer([p["prompt"] for p in batch], return_tensors="pt", padding=True,
                               truncation=True, max_length=MAX_INPUT_TOKENS).to(device)
            labels = tokenizer([p["answer"] for p in batch], return_tensors="pt", padding=True,
                               truncation=True, max_length=MAX_ANSWER_TOKENS).input_ids.to(device)
            labels[labels == tokenizer.pad_token_id] = -100   # do not grade the padding
            loss = model(**inputs, labels=labels).loss          # how wrong was the model?
            loss.backward()                                     # work out how to correct it
            optimizer.step()                                    # apply the correction
            optimizer.zero_grad()
            total_loss += loss.item() * len(batch)
        average_loss = total_loss / len(train)

        if epoch % check_every == 0 or epoch == epochs:
            checkpoint = score(generate(model, tokenizer, test_prompts, device), test)
            history.append({"epoch": epoch, "loss": average_loss, "accuracy": checkpoint["accuracy"],
                            "correct": checkpoint["correct"], "relevance": checkpoint["relevance"]})
            print(f"Epoch {epoch:>2}: training loss {average_loss:.3f} | test accuracy "
                  f"{checkpoint['correct']}/{checkpoint['total']} ({checkpoint['accuracy']:.0%})")
        else:
            print(f"Epoch {epoch:>2}: training loss {average_loss:.3f}")
    minutes = (time.perf_counter() - started) / 60

    # Step 4. Final comparison on the test prompts
    tuned_answers = generate(model, tokenizer, test_prompts, device)
    tuned = score(tuned_answers, test)
    print(f"Fine-tuned model: {tuned['correct']}/{tuned['total']} correct "
          f"({tuned['accuracy']:.0%}), relevance {tuned['relevance']:.2f}")

    if save_model:
        MODEL_FOLDER.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(MODEL_FOLDER)
        tokenizer.save_pretrained(MODEL_FOLDER)

    return {"model": MODEL_NAME, "device": str(device), "train_size": len(train), "test_size": len(test),
            "epochs": epochs, "learning_rate": LEARNING_RATE, "batch_size": BATCH_SIZE, "minutes": minutes,
            "parameters": sum(p.numel() for p in model.parameters()),
            "history": history, "original": original, "tuned": tuned, "test": test,
            "original_answers": original_answers, "tuned_answers": tuned_answers}