"""
SBA 928: Enhancing Market Research with AI Prompt Engineering
Student: Anthony Emmanuel

How to run (from the project folder):
    uv run sba-928-market-research --part prompts    # Requirements 1-2: dataset, prompts, variations
    uv run sba-928-market-research --part finetune   # Requirements 3-4: fine-tune and compare
    uv run sba-928-market-research --part bias       # Requirements 5-6: bias and fairness checks
    uv run sba-928-market-research                   # everything

Every result is saved as a Markdown table in the results/ folder.
"""

import argparse
import json
from collections import Counter
from pathlib import Path

from sba_928_market_research import bias, finetune, prompts as prompt_builder
from sba_928_market_research.data import load_facts

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
RESULTS_FOLDER = PROJECT_FOLDER / "results"
FINETUNE_JSON = RESULTS_FOLDER / "finetune_results.json"


def md_table(headers, rows):
    def clean(cell):
        return str(cell).replace("|", "\\|").replace("\n", " ")

    lines = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(clean(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def save(filename, title, sections):
    RESULTS_FOLDER.mkdir(exist_ok=True)
    (RESULTS_FOLDER / filename).write_text(f"# {title}\n\n" + "\n\n".join(sections) + "\n", encoding="utf-8")
    print(f"Saved: results/{filename}")


def ratio(pair):
    correct, total = pair
    return f"{correct}/{total} ({correct / total:.0%})" if total else "0/0"


# ---------------------------------------------------------------
# Requirements 1 and 2
# ---------------------------------------------------------------
def run_prompts(facts, sales, report, prompts):
    print("\n=== Requirements 1-2: Dataset, curated prompts and variations ===")
    summary = [
        ["Source", "UCI Machine Learning Repository, Online Retail (dataset 352)"],
        ["Period covered", f"{report['first_date']:%B %d, %Y} to {report['last_date']:%B %d, %Y}"],
        ["Rows in the file", f"{report['raw_rows']:,}"],
        ["Product sales rows after cleaning", f"{report['sales_rows']:,}"],
        ["Cancelled rows removed", f"{report['cancelled_rows']:,}"],
        ["Orders reversed by a cancellation, removed", f"{report['reversed_rows']:,}"],
        ["Countries", sales["Country"].nunique()],
        ["Different products", f"{sales['Description'].nunique():,}"],
        ["Identified customers", f"{sales['CustomerID'].nunique():,}"],
    ]
    category_counts = Counter(f["category"] for f in facts)
    save("01_dataset_and_facts.md", "Requirement 1: The sourced dataset and the facts behind the prompts", [
        "## Dataset summary", md_table(["Item", "Value"], summary),
        "## Facts per market research area",
        md_table(["Area", "Facts", "Prompts (6 per fact)"], [[c, n, n * 6] for c, n in category_counts.items()]),
        "## Every fact with its correct insight",
        md_table(["ID", "Area", "Market", "Question", "Correct insight"],
                 [[f["id"], f["category"], f["group"], f["q1"], f["answer"]] for f in facts]),
    ])

    prompt_builder.save_prompts(prompts, RESULTS_FOLDER / "market_research_prompts.csv")
    print(f"Saved: results/market_research_prompts.csv ({len(prompts)} prompts)")

    example_ids = [next(f["id"] for f in facts if f["category"] == c) for c in category_counts]
    sections = ["## The six techniques",
                md_table(["Technique", "Used for", "When to use it in market research"],
                         [[name, "Testing" if name == prompt_builder.TEST_TECHNIQUE else "Training", use]
                          for name, (_, _, use) in prompt_builder.TECHNIQUES.items()])]
    for fact_id in example_ids:
        rows = [[p["technique"], p["prompt"]] for p in prompts if p["fact_id"] == fact_id]
        fact = next(f for f in facts if f["id"] == fact_id)
        sections += [f"## Example from {fact['category']} (correct insight: {fact['answer']})",
                     md_table(["Technique", "Prompt"], rows)]
    save("02_prompt_variations.md", "Requirement 2: Prompt variations", sections)
    print(f"Facts: {len(facts)} | Prompts: {len(prompts)} | Areas: {dict(category_counts)}")


# ---------------------------------------------------------------
# Requirements 3 and 4
# ---------------------------------------------------------------
def run_finetune(prompts):
    print("\n=== Requirements 3-4: Fine-tuning experiment and comparison ===")
    result = finetune.run_experiment(prompts)
    original, tuned, test = result["original"], result["tuned"], result["test"]

    process = [
        ["Model", f"{result['model']} ({result['parameters'] / 1e6:.0f} million parameters)"],
        ["Training examples", f"{result['train_size']} prompts (5 techniques for every fact)"],
        ["Test examples", f"{result['test_size']} prompts (the paraphrase technique, never seen in training)"],
        ["Epochs", result["epochs"]], ["Learning rate", result["learning_rate"]],
        ["Batch size", result["batch_size"]], ["Device", result["device"]],
        ["Training time", f"{result['minutes']:.1f} minutes"],
    ]
    save("03_finetuning_process.md", "Requirement 3: The fine-tuning experiment", [
        "## Setup", md_table(["Setting", "Value"], process),
        "## Progress during training (tested on the unseen prompts)",
        md_table(["Epoch", "Training loss", "Test accuracy", "Relevance"],
                 [[h["epoch"], f"{h['loss']:.3f}", f"{h['correct']}/{result['test_size']} ({h['accuracy']:.0%})",
                   f"{h['relevance']:.2f}"] for h in result["history"]]),
    ])

    categories = sorted(original["by_category"])
    groups = sorted(original["by_group"])
    examples = [[t["prompt"], t["answer"], o, n, "Yes" if ok else "No"]
                for t, o, n, ok in zip(test, result["original_answers"], result["tuned_answers"], tuned["is_correct"])]
    save("04_model_comparison.md", "Requirement 4: Original model compared with the fine-tuned model", [
        "## Overall",
        md_table(["Model", "Correct", "Accuracy", "Relevance (word overlap, 0 to 1)"],
                 [["Original flan-t5-small", f"{original['correct']}/{original['total']}", f"{original['accuracy']:.0%}", f"{original['relevance']:.2f}"],
                  ["Fine-tuned", f"{tuned['correct']}/{tuned['total']}", f"{tuned['accuracy']:.0%}", f"{tuned['relevance']:.2f}"]]),
        "## Accuracy by market research area",
        md_table(["Area", "Original", "Fine-tuned"],
                 [[c, ratio(original["by_category"][c]), ratio(tuned["by_category"][c])] for c in categories]),
        "## Accuracy by market (fairness check)",
        md_table(["Market", "Original", "Fine-tuned"],
                 [[g, ratio(original["by_group"][g]), ratio(tuned["by_group"][g])] for g in groups]),
        "## Every test prompt, side by side",
        md_table(["Test prompt", "Correct insight", "Original model", "Fine-tuned model", "Fine-tuned correct?"], examples),
    ])

    FINETUNE_JSON.write_text(json.dumps({
        "by_group": {g: {"original": original["by_group"][g], "tuned": tuned["by_group"][g]} for g in groups},
        "by_category": {c: {"original": original["by_category"][c], "tuned": tuned["by_category"][c]} for c in categories},
    }, indent=2), encoding="utf-8")


# ---------------------------------------------------------------
# Requirements 5 and 6
# ---------------------------------------------------------------
def run_bias(sales, report, prompts):
    print("\n=== Requirements 5-6: Bias assessment and fairness checks ===")
    coverage = bias.prompt_coverage(prompts, sales)
    flagged, examples = bias.audit_wording(prompts)

    last_day = report["last_date"]
    data_notes = [
        ["Home market dominance", f"The United Kingdom is {coverage['uk_share_of_data_rows']:.0%} of sales rows",
         "Totals and averages mostly describe UK customers"],
        ["Missing customer IDs", f"{report['rows_without_customer'] / report['sales_rows']:.0%} of sales rows have no customer ID",
         "Customer behavior findings leave these buyers out"],
        ["Incomplete final month", f"Data ends on {last_day:%B %d, %Y}",
         "The last month looks weak unless it is treated as partial"],
        ["No demographic fields", "Age, gender and income are not recorded",
         "Prompts must not assume who the customers are"],
        ["One company only", "All rows come from a single retailer",
         "Findings describe this retailer, not the whole market or its competitors"],
    ]
    sections = [
        "## 1. Data bias: who is represented in the dataset",
        md_table(["Market", "Share of sales rows", "Share of revenue", "Share of customers"], bias.data_representation(sales)),
        md_table(["Risk", "Evidence", "Effect on insights"], data_notes),
        "## 2. Prompt bias: coverage",
        md_table(["Market research area", "Prompts"], coverage["by_category"].items()),
        md_table(["Market the prompt is about", "Prompts"], coverage["by_group"].items()),
        f"The United Kingdom is {coverage['uk_share_of_data_rows']:.0%} of the data rows but "
        f"{coverage['uk_share_of_market_prompts']:.0%} of the prompts about a specific market. "
        "The prompt set was balanced on purpose so smaller markets are not ignored.",
        "## 3. Prompt bias: leading language",
        f"Curated prompts checked: {len(prompts)}. Prompts flagged: {len(flagged)}.",
        md_table(["Biased prompt", "Problem", "Detector found", "Fair rewrite", "Rewrite flagged?"],
                 [[b, why, ", ".join(found) or "nothing", fair, "Yes" if fair_found else "No"]
                  for b, fair, why, found, fair_found in examples]),
    ]
    if flagged:
        sections.append(md_table(["Prompt ID", "Prompt", "Found"], [[i, p, ", ".join(f)] for i, p, f in flagged]))

    if FINETUNE_JSON.exists():
        by_group = json.loads(FINETUNE_JSON.read_text(encoding="utf-8"))["by_group"]
        sections += ["## 4. Model bias: accuracy by market",
                     md_table(["Market", "Original model", "Fine-tuned model"],
                              [[g, ratio(v["original"]), ratio(v["tuned"])] for g, v in by_group.items()])]
    else:
        sections.append("## 4. Model bias\n\nRun `--part finetune` first to add accuracy by market.")
    save("05_bias_and_fairness.md", "Requirements 5-6: Bias assessment and fairness checks", sections)

    caught = sum(1 for *_, found, _ in examples if found)
    print(f"UK share of data rows: {coverage['uk_share_of_data_rows']:.0%} | "
          f"UK share of market-specific prompts: {coverage['uk_share_of_market_prompts']:.0%}")
    print(f"Leading-language check: {len(flagged)} of {len(prompts)} curated prompts flagged | "
          f"{caught} of {len(examples)} biased examples caught")


def main():
    parser = argparse.ArgumentParser(description="SBA 928 market research with AI prompt engineering")
    parser.add_argument("--part", choices=["all", "prompts", "finetune", "bias"], default="all")
    part = parser.parse_args().part

    facts, sales, report = load_facts()
    prompts = prompt_builder.build_prompts(facts)
    print(f"Loaded {report['sales_rows']:,} product sales rows and built {len(prompts)} prompts from {len(facts)} facts")

    if part in ("all", "prompts"):
        run_prompts(facts, sales, report, prompts)
    if part in ("all", "finetune"):
        run_finetune(prompts)
    if part in ("all", "bias"):
        run_bias(sales, report, prompts)


if __name__ == "__main__":
    main()