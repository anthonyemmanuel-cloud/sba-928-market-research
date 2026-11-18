"""
Requirements 1 and 2: the curated prompt dataset and its variations.

Every fact from data.py becomes SIX prompts, one for each prompting
technique below. Five techniques are used to train the model. The sixth
(a rewording the model has never seen) is held back to test it.
"""

import csv

COMPANY = "a UK online gift retailer"
PERIOD = "December 2010 to December 2011"


def lower_first(text):
    return text[0].lower() + text[1:]


# technique name -> (which wording of the question it uses, how the prompt is built, when to use it)
TECHNIQUES = {
    "direct": ("q1", lambda q: q,
               "A plain question. Fast lookups when the analyst already knows the context."),
    "role": ("q1", lambda q: f"You are a market research analyst at {COMPANY}. {q}",
             "Gives the AI a job, so answers use the right point of view and vocabulary."),
    "context": ("q2", lambda q: f"Our firm is reviewing its sales data from {PERIOD} to plan next year's strategy. {q}",
                "Adds background and purpose, so the answer fits the business decision."),
    "format": ("q2", lambda q: f"{q} Answer in one short sentence and name the specific figure or item.",
               "Controls the shape of the answer, so results can go straight into a report or table."),
    "audience": ("q1", lambda q: f"A senior executive with no technical background asks: {lower_first(q)}",
                 "Sets the reader, so the answer is in plain business language."),
    "paraphrase": ("q3", lambda q: q,
                   "A new wording of the same question. Checks that the insight does not depend on exact phrasing."),
}
TRAIN_TECHNIQUES = ["direct", "role", "context", "format", "audience"]
TEST_TECHNIQUE = "paraphrase"


def build_prompts(facts):
    prompts = []
    for fact in facts:
        for technique, (wording, make, _) in TECHNIQUES.items():
            prompts.append({
                "prompt_id": f"{fact['id']}-{technique}",
                "fact_id": fact["id"],
                "category": fact["category"],
                "group": fact["group"],
                "technique": technique,
                "split": "test" if technique == TEST_TECHNIQUE else "train",
                "prompt": make(fact[wording]),
                "answer": fact["answer"],
                "key": fact["key"],
            })
    return prompts


def save_prompts(prompts, path):
    path.parent.mkdir(exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(prompts[0].keys()))
        writer.writeheader()
        writer.writerows(prompts)