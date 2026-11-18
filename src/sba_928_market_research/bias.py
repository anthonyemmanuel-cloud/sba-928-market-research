"""
Requirements 5 and 6: bias assessment and fairness checks.

Three checks that all produce numbers:
    1. Data bias     - is one market over-represented in the dataset?
    2. Prompt bias   - do the prompts cover every market and category,
                       and is any prompt worded in a leading way?
    3. Model bias    - is the fine-tuned model less accurate for some
                       markets than others? (calculated in finetune.py)
"""

import re
from collections import Counter

from sba_928_market_research.data import UK

# Words and phrases that push the AI toward an answer or carry a stereotype
LEADING_PATTERNS = {
    "assumes the answer": r"\b(obviously|clearly|of course|everyone knows|as we all know|undoubtedly)\b",
    "asks for one side only": r"\b(prove that|confirm that|explain why .* (is|are) (the )?(best|worst|better|superior|failing))\b",
    "absolute wording": r"\b(always|never|all customers|every customer|no one|nobody)\b",
    "stereotype about a group": r"\b(housewives|millennials are|older people (can't|cannot|don't)|foreign(ers)?|cheap customers|women (prefer|love|buy)|men (prefer|love|buy))\b",
    "home market treated as the norm": r"\b(normal customers|real customers|our main customers|typical british)\b",
}

# Deliberately biased prompts with a fair rewrite of each (used to test the detector
# and as examples in the report)
BIASED_EXAMPLES = [
    ("Explain why the United Kingdom is the best market we have.",
     "Compare the United Kingdom with our other markets on revenue, average order value and repeat orders.",
     "Assumes the conclusion and asks for one side only"),
    ("Obviously overseas customers are less loyal. How do we fix that?",
     "What share of customers in each country ordered more than once?",
     "States an untested claim about a group as fact"),
    ("Which products do women buy as gifts for the home?",
     "Which products sell the most units, and what do we know and not know about who buys them?",
     "Assumes gender, which the dataset does not record"),
    ("Customers always order more before Christmas. Confirm that our sales follow this.",
     "How does monthly revenue change across the year, and which months are highest and lowest?",
     "Absolute wording and asks only for confirmation"),
    ("What do normal customers spend compared with foreign buyers?",
     "What is the average order value in each country?",
     "Treats the home market as the norm and others as outsiders"),
    ("Prove that our cheap customers are not worth serving.",
     "How is revenue spread across small, medium and large customers?",
     "Loaded label and one sided request"),
]


def find_leading_language(prompt):
    # Returns the list of bias types found in one prompt (empty list = none found)
    return [label for label, pattern in LEADING_PATTERNS.items() if re.search(pattern, prompt.lower())]


def data_representation(sales):
    # How much of the dataset does each market make up?
    by_country = sales.groupby("Country").agg(Rows=("Revenue", "size"), Revenue=("Revenue", "sum"),
                                              Customers=("CustomerID", "nunique"))
    totals = by_country.sum()
    rows = []
    for country, r in by_country.sort_values("Revenue", ascending=False).head(8).iterrows():
        rows.append([country, f"{r['Rows'] / totals['Rows']:.1%}", f"{r['Revenue'] / totals['Revenue']:.1%}",
                     f"{r['Customers'] / totals['Customers']:.1%}"])
    others = by_country.sort_values("Revenue", ascending=False).iloc[8:].sum()
    rows.append([f"All other countries ({max(len(by_country) - 8, 0)})", f"{others['Rows'] / totals['Rows']:.1%}",
                 f"{others['Revenue'] / totals['Revenue']:.1%}", f"{others['Customers'] / totals['Customers']:.1%}"])
    return rows


def prompt_coverage(prompts, sales):
    # Compare how often each market appears in the PROMPTS with its share of the DATA
    uk_data_share = (sales["Country"] == UK).mean()
    groups = Counter(p["group"] for p in prompts)
    market_specific = groups["UK"] + groups["Non-UK"]
    return {
        "by_category": Counter(p["category"] for p in prompts),
        "by_technique": Counter(p["technique"] for p in prompts),
        "by_group": groups,
        "uk_share_of_data_rows": uk_data_share,
        "uk_share_of_market_prompts": groups["UK"] / market_specific if market_specific else 0.0,
    }


def audit_wording(prompts):
    # Check every curated prompt and every biased example for leading language
    flagged = [(p["prompt_id"], p["prompt"], found) for p in prompts if (found := find_leading_language(p["prompt"]))]
    examples = [(biased, fair, why, find_leading_language(biased), find_leading_language(fair))
                for biased, fair, why in BIASED_EXAMPLES]
    return flagged, examples