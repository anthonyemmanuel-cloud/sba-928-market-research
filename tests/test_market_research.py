"""
Automated tests for the SBA 928 project.

They use a tiny made-up sales table where the right answers are known,
so they run in seconds without the real dataset, a model or the internet.

Run them with:
    uv run pytest
"""

import pandas as pd
import pytest

from sba_928_market_research import bias, finetune, prompts
from sba_928_market_research.data import build_facts, clean, money, percent


@pytest.fixture(scope="module")
def tiny():
    rows = []

    def sale(invoice, code, product, quantity, date, price, customer, country):
        rows.append({"InvoiceNo": invoice, "StockCode": code, "Description": product, "Quantity": quantity,
                     "InvoiceDate": pd.Timestamp(date), "UnitPrice": price, "CustomerID": customer, "Country": country})

    sale("1001", "10001", "RED MUG ", 10, "2011-01-03 10:00", 2.0, 1.0, "United Kingdom")    # 20
    sale("1001", "10002", "BLUE PLATE", 5, "2011-01-03 10:00", 4.0, 1.0, "United Kingdom")   # 20
    sale("1002", "10001", "RED MUG", 30, "2011-02-08 12:00", 2.0, 1.0, "United Kingdom")     # 60
    sale("1003", "10002", "BLUE PLATE", 50, "2011-02-09 12:00", 4.0, 2.0, "Germany")         # 200
    sale("1004", "10003", "GREEN BOWL", 4, "2011-03-10 15:00", 5.0, None, "France")          # 20
    sale("C1005", "10001", "RED MUG", -3, "2011-03-11 09:00", 2.0, 1.0, "United Kingdom")    # cancellation
    sale("1006", "POST", "POSTAGE", 1, "2011-03-11 09:00", 18.0, 2.0, "Germany")             # not a product
    sale("1007", "10003", "GREEN BOWL", 900, "2011-03-12 09:00", 5.0, 3.0, "France")         # huge order...
    sale("C1008", "10003", "GREEN BOWL", -900, "2011-03-12 10:00", 5.0, 3.0, "France")       # ...cancelled
    sales, report = clean(pd.DataFrame(rows))
    return sales, report, build_facts(sales, report)


def answer_to(facts, question):
    return next(f for f in facts if f["q1"] == question)


# ---------- Requirement 1: data and facts ----------

def test_cleaning_removes_cancellations_and_postage(tiny):
    sales, report, _ = tiny
    assert len(sales) == 5
    assert report["cancelled_rows"] == 2
    assert report["reversed_rows"] == 1          # the 900-bowl order that was cancelled
    assert set(sales["Description"]) == {"Red Mug", "Blue Plate", "Green Bowl"}   # tidied names


def test_facts_match_hand_calculated_answers(tiny):
    _, _, facts = tiny
    assert answer_to(facts, "Which month had the highest sales revenue?")["key"] == "February 2011"
    assert answer_to(facts, "What share of total revenue comes from the United Kingdom?")["key"] == "31 percent"
    assert answer_to(facts, "Which product is the top earner by revenue?")["key"] == "Blue Plate"
    assert answer_to(facts, "Which country is the largest market by revenue outside the United Kingdom?")["key"] == "Germany"
    assert answer_to(facts, "What is the average order value?")["key"] == "80 pounds"


def test_facts_cover_all_four_research_areas(tiny):
    _, _, facts = tiny
    assert {f["category"] for f in facts} == {"Market trends", "Consumer behavior", "Regional markets", "Competitive positioning"}
    assert all(f["key"].lower() in f["answer"].lower() for f in facts)   # every answer contains its key fact


def test_number_formatting():
    assert money(8_234_567) == "8.2 million pounds"
    assert money(45_400) == "45 thousand pounds"
    assert money(458.3) == "458 pounds"
    assert percent(0.826) == "83 percent"


def test_comparison_answer_is_not_always_in_the_same_position(tiny):
    # Position bias fix: the two training wordings name the right answer in opposite places
    _, _, facts = tiny
    comparisons = [f for f in facts if f["q1"].startswith("Which earns more revenue")]
    assert comparisons
    for f in comparisons:
        assert (f["q1"].index(f["key"]) < len(f["q1"]) / 2) != (f["q2"].index(f["key"]) < len(f["q2"]) / 2)


# ---------- Requirement 2: prompt variations ----------

def test_six_variations_per_fact(tiny):
    _, _, facts = tiny
    built = prompts.build_prompts(facts)
    assert len(built) == len(facts) * 6
    assert len({p["prompt"] for p in built if p["fact_id"] == "M01"}) == 6   # all six are different


def test_test_prompts_are_never_in_training(tiny):
    _, _, facts = tiny
    built = prompts.build_prompts(facts)
    train = {p["prompt"] for p in built if p["split"] == "train"}
    test = {p["prompt"] for p in built if p["split"] == "test"}
    assert test and not (train & test)


# ---------- Requirement 4: scoring ----------

def test_is_correct_needs_the_whole_key():
    assert finetune.is_correct("About 8 percent of invoices are cancellations.", "8 percent")
    assert not finetune.is_correct("About 18 percent of invoices are cancellations.", "8 percent")
    assert finetune.is_correct("the top market is GERMANY", "Germany")


def test_overlap_f1():
    assert finetune.overlap_f1("Sales peaked in November 2011.", "Sales peaked in November 2011.") == 1.0
    assert finetune.overlap_f1("bananas", "Sales peaked in November 2011.") == 0.0


def test_score_breaks_results_down_by_market():
    records = [{"key": "Germany", "answer": "It is Germany.", "category": "Regional markets", "group": "Non-UK"},
               {"key": "83 percent", "answer": "About 83 percent.", "category": "Regional markets", "group": "UK"}]
    result = finetune.score(["It is Germany.", "About 50 percent."], records)
    assert result["correct"] == 1 and result["accuracy"] == 0.5
    assert result["by_group"] == {"Non-UK": (1, 1), "UK": (0, 1)}


# ---------- Requirements 5 and 6: bias ----------

def test_detector_catches_every_biased_example_and_no_fair_rewrite():
    for biased, fair, _ in bias.BIASED_EXAMPLES:
        assert bias.find_leading_language(biased), biased
        assert not bias.find_leading_language(fair), fair


def test_curated_prompts_have_no_leading_language(tiny):
    _, _, facts = tiny
    flagged, _ = bias.audit_wording(prompts.build_prompts(facts))
    assert flagged == []


def test_prompt_coverage_compares_data_share_with_prompt_share(tiny):
    sales, _, facts = tiny
    coverage = bias.prompt_coverage(prompts.build_prompts(facts), sales)
    assert coverage["uk_share_of_data_rows"] == 0.6           # 3 of 5 sales rows
    assert 0 < coverage["uk_share_of_market_prompts"] < 1