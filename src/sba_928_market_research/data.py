"""
Requirement 1 (first half): the sourced dataset.

Dataset: "Online Retail" from the UCI Machine Learning Repository
(https://archive.ics.uci.edu/dataset/352/online+retail, license CC BY 4.0).
It holds every transaction of a UK online gift retailer from
December 1, 2010 to December 9, 2011 (about 540,000 rows, 38 countries).

This module loads the file, cleans it, and calculates the FACTS that the
market research prompts ask about. Because every fact is calculated from
the data, we always know the correct answer to every prompt.
"""

import os
import random
from pathlib import Path

import pandas as pd

PROJECT_FOLDER = Path(__file__).resolve().parents[2]
# The data folder can be changed with an environment variable (used by the tests)
DATA_FOLDER = Path(os.getenv("SBA928_DATA_DIR", PROJECT_FOLDER / "data"))

UK = "United Kingdom"


# ---------------------------------------------------------------
# Load and clean
# ---------------------------------------------------------------
def load_raw():
    # Reading the Excel file takes a minute or two, so the first run saves
    # a CSV copy that loads in a few seconds the next time.
    cache = DATA_FOLDER / "online_retail.csv"
    if cache.exists():
        return pd.read_csv(cache, dtype={"InvoiceNo": str, "StockCode": str}, parse_dates=["InvoiceDate"])

    excel_files = sorted(DATA_FOLDER.glob("*.xlsx"))
    if not excel_files:
        raise SystemExit(
            "Dataset not found. Download 'Online Retail.xlsx' from the UCI repository "
            "into the data folder (see the README, 'How to get the dataset')."
        )
    print(f"Reading {excel_files[0].name} (this takes a minute or two the first time)...")
    df = pd.read_excel(excel_files[0], dtype={"InvoiceNo": str, "StockCode": str})
    df.to_csv(cache, index=False)
    return df


def find_reversed_orders(df, cancelled):
    # Returns True for each sale row that a later cancellation undoes in full.
    # Matching counts are kept, so 2 cancellations remove at most 2 matching sales.
    keys = ["CustomerID", "StockCode", "Units"]
    rows = df.assign(Units=df["Quantity"].abs())
    known = rows["CustomerID"].notna()
    sales = rows[~cancelled & known & (rows["Quantity"] > 0)].sort_values("InvoiceDate")
    cancels = rows[cancelled & known & (rows["Quantity"] < 0)]
    allowed = cancels.groupby(keys).size()                       # how many cancellations per key
    order = sales.groupby(keys).cumcount()                       # 0 for the first matching sale, 1 for the next...
    limit = sales.set_index(keys).index.map(lambda key: allowed.get(key, 0))
    reversed_rows = pd.Series(False, index=df.index)
    reversed_rows[sales.index[order.to_numpy() < limit.to_numpy()]] = True
    return reversed_rows


def clean(df):
    # Returns (sales, report). `sales` holds only real product sales.
    df = df.copy()
    df["Description"] = df["Description"].astype("string").str.strip().str.title()
    df["Country"] = df["Country"].astype("string").str.strip()
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    cancelled = df["InvoiceNo"].str.startswith("C")                 # cancelled orders start with "C"
    is_product = df["StockCode"].str.match(r"^\d{5}")                # skip postage, fees, manual adjustments
    valid = (df["Quantity"] > 0) & (df["UnitPrice"] > 0) & df["Description"].notna()

    # A cancellation is its own row, but the ORIGINAL order row is still in the data.
    # Remove each original order that a cancellation fully reverses: same customer,
    # same product, same quantity. Example: an order of 80,995 paper birds that was
    # cancelled the same day would otherwise look like the best-selling product.
    reversed_orders = find_reversed_orders(df, cancelled)
    sales = df[~cancelled & is_product & valid & ~reversed_orders].copy()

    sales["Month"] = sales["InvoiceDate"].dt.to_period("M")
    sales["Weekday"] = sales["InvoiceDate"].dt.day_name()
    sales["Hour"] = sales["InvoiceDate"].dt.hour

    report = {
        "raw_rows": len(df),
        "sales_rows": len(sales),
        "cancelled_rows": int(cancelled.sum()),
        "cancelled_invoices": int(df.loc[cancelled, "InvoiceNo"].nunique()),
        "reversed_rows": int(reversed_orders.sum()),
        "all_invoices": int(df["InvoiceNo"].nunique()),
        "rows_without_customer": int(sales["CustomerID"].isna().sum()),
        "first_date": df["InvoiceDate"].min(),
        "last_date": df["InvoiceDate"].max(),
    }
    return sales, report


# ---------------------------------------------------------------
# Number formatting (kept simple so a small model can learn it)
# ---------------------------------------------------------------
def money(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} million pounds"
    if value >= 10_000:
        return f"{round(value / 1000):,} thousand pounds"
    return f"{round(value):,} pounds"


def percent(share):
    return f"{round(share * 100)} percent"


def month_name(period):
    return period.strftime("%B %Y")


# ---------------------------------------------------------------
# Build the facts
# ---------------------------------------------------------------
def build_facts(sales, report):
    # Each fact is one market research finding with:
    #   category  - the market research area it belongs to
    #   group     - which market it is about (UK, Non-UK or Global), used for the fairness check
    #   q1,q2,q3  - three different ways to ask the question
    #   answer    - the correct one-sentence insight
    #   key       - the exact value that must appear for an answer to count as correct
    facts = []

    def add(category, group, q1, q2, q3, answer, key):
        facts.append({"id": f"M{len(facts) + 1:02d}", "category": category, "group": group,
                      "q1": q1, "q2": q2, "q3": q3, "answer": answer, "key": str(key)})

    TRENDS, BEHAVIOR, REGIONAL, POSITION = ("Market trends", "Consumer behavior",
                                            "Regional markets", "Competitive positioning")

    revenue_total = sales["Revenue"].sum()
    by_month = sales.groupby("Month")["Revenue"].sum()
    last_month = sales["Month"].max()
    # The final month is only partly recorded, so leave it out of "lowest month" comparisons
    last_is_partial = sales.loc[sales["Month"] == last_month, "InvoiceDate"].dt.day.max() < 25
    full_months = by_month.drop(last_month) if last_is_partial else by_month
    orders = sales.groupby("InvoiceNo").agg(Revenue=("Revenue", "sum"), Items=("Quantity", "sum"),
                                            Country=("Country", "first"), Customer=("CustomerID", "first"))

    # ----- Market trends -----
    best_month, worst_month = full_months.idxmax(), full_months.idxmin()
    add(TRENDS, "Global", "Which month had the highest sales revenue?",
        "In which month did sales revenue peak?", "What was the strongest month for revenue?",
        f"Sales revenue peaked in {month_name(best_month)}.", month_name(best_month))
    add(TRENDS, "Global", "Which full month had the lowest sales revenue?",
        "In which full month was sales revenue at its lowest?", "What was the weakest full month for revenue?",
        f"The lowest full month for sales revenue was {month_name(worst_month)}.", month_name(worst_month))

    by_weekday = sales.groupby("Weekday")["Revenue"].sum()
    add(TRENDS, "Global", "Which day of the week brings in the most revenue?",
        "On which weekday is sales revenue highest?", "What is the best weekday for sales?",
        f"{by_weekday.idxmax()} brings in the most revenue of any weekday.", by_weekday.idxmax())
    all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    missing_days = [d for d in all_days if d not in by_weekday.index]
    if missing_days:
        add(TRENDS, "Global", "On which day of the week are no sales recorded?",
            "Which weekday has no sales at all in the data?", "Is there a weekday when the retailer records no sales?",
            f"No sales are recorded on {missing_days[0]}.", missing_days[0])

    peak_hour = sales.groupby("Hour")["InvoiceNo"].nunique().idxmax()
    add(TRENDS, "Global", "At what hour of the day are the most orders placed?",
        "Which hour of the day is busiest for orders?", "When during the day do customers order the most?",
        f"The busiest hour for orders starts at {peak_hour}:00.", f"{peak_hour}:00")

    by_quarter = sales.groupby(sales["InvoiceDate"].dt.to_period("Q"))["Revenue"].sum()
    best_quarter = by_quarter.idxmax()
    quarter_text = f"quarter {best_quarter.quarter} of {best_quarter.year}"
    add(TRENDS, "Global", "Which quarter had the highest sales revenue?",
        "In which quarter did the retailer earn the most?", "What was the strongest quarter for revenue?",
        f"The strongest quarter for revenue was {quarter_text}.", quarter_text)

    add(TRENDS, "Global", "What was the total sales revenue for the whole period?",
        "How much sales revenue did the retailer earn in total?", "What do total sales add up to across the full dataset?",
        f"Total sales revenue for the period was about {money(revenue_total)}.", money(revenue_total).replace(" pounds", ""))

    top_by_month = sales.groupby(["Month", "Description"])["Quantity"].sum()
    for month in by_month.index:
        product = top_by_month.loc[month].idxmax()
        name = month_name(month)
        add(TRENDS, "Global", f"What was the best-selling product by units in {name}?",
            f"Which product sold the most units in {name}?", f"In {name}, which item was the top seller by quantity?",
            f"The best-selling product in {name} was {product}.", product)

    # ----- Consumer behavior -----
    add(BEHAVIOR, "Global", "What is the average order value?",
        "How much does a customer spend on an average order?", "What does a typical order come to on average?",
        f"The average order value is about {money(orders['Revenue'].mean())}.", money(orders["Revenue"].mean()))
    add(BEHAVIOR, "Global", "What is the median order value?",
        "What is the middle order value when all orders are ranked?", "How large is the median order?",
        f"The median order value is about {money(orders['Revenue'].median())}.", money(orders["Revenue"].median()))
    add(BEHAVIOR, "Global", "How many items does an average order contain?",
        "What is the average number of units per order?", "How many units do customers buy in a typical order on average?",
        f"An average order contains about {round(orders['Items'].mean())} items.", f"{round(orders['Items'].mean())} items")

    cancel_rate = report["cancelled_invoices"] / report["all_invoices"]
    add(BEHAVIOR, "Global", "What share of all invoices are cancellations?",
        "What percentage of invoices were cancelled?", "How common are cancelled orders as a share of invoices?",
        f"About {percent(cancel_rate)} of all invoices are cancellations.", percent(cancel_rate))

    known = orders.dropna(subset=["Customer"])
    per_customer = known.groupby("Customer").agg(Orders=("Revenue", "size"), Revenue=("Revenue", "sum"))
    repeat = (per_customer["Orders"] > 1).mean()
    add(BEHAVIOR, "Global", "What share of identified customers ordered more than once?",
        "What percentage of known customers are repeat buyers?", "How many identified customers came back for a second order, as a share?",
        f"About {percent(repeat)} of identified customers ordered more than once.", percent(repeat))
    add(BEHAVIOR, "Global", "How many orders does an identified customer place on average?",
        "What is the average number of orders per known customer?", "On average, how often does an identified customer order?",
        f"An identified customer places about {per_customer['Orders'].mean():.1f} orders on average.",
        f"{per_customer['Orders'].mean():.1f} orders")
    top_tenth = per_customer["Revenue"].sort_values(ascending=False).head(max(1, len(per_customer) // 10)).sum()
    top_share = top_tenth / per_customer["Revenue"].sum()
    add(BEHAVIOR, "Global", "What share of customer revenue comes from the top 10 percent of customers?",
        "How much of identified customer revenue do the top tenth of customers generate?",
        "How concentrated is revenue among the biggest 10 percent of customers?",
        f"The top 10 percent of customers generate about {percent(top_share)} of identified customer revenue.", percent(top_share))
    unknown_share = report["rows_without_customer"] / report["sales_rows"]
    add(BEHAVIOR, "Global", "What share of sales lines have no customer ID?",
        "What percentage of sales records cannot be linked to a customer?", "How much of the sales data is missing a customer ID?",
        f"About {percent(unknown_share)} of sales lines have no customer ID.", percent(unknown_share))

    by_country = sales[sales["Country"] != "Unspecified"].groupby("Country")["Revenue"].sum().sort_values(ascending=False)
    top_countries = list(by_country.index[:8])
    for country in top_countries:
        value = orders.loc[orders["Country"] == country, "Revenue"].mean()
        group = "UK" if country == UK else "Non-UK"
        add(BEHAVIOR, group, f"What is the average order value for customers in {country}?",
            f"How much does an average order from {country} come to?", f"In {country}, what does a typical order average?",
            f"The average order value in {country} is about {money(value)}.", money(value))

    # ----- Regional markets -----
    uk_share = by_country.get(UK, 0) / by_country.sum()
    add(REGIONAL, "UK", "What share of total revenue comes from the United Kingdom?",
        "What percentage of revenue is generated in the United Kingdom?", "How much of the retailer's revenue is from United Kingdom customers?",
        f"The United Kingdom generates about {percent(uk_share)} of total revenue.", percent(uk_share))
    add(REGIONAL, "Global", "How many countries does the retailer sell to?",
        "In how many countries does the retailer have sales?", "What is the number of countries with recorded sales?",
        f"The retailer has sales in {sales['Country'].nunique()} countries.", f"{sales['Country'].nunique()} countries")

    abroad = by_country.drop(UK, errors="ignore")
    ranks = ["largest", "second largest", "third largest", "fourth largest", "fifth largest"]
    for rank, country in zip(ranks, abroad.index[:5]):
        add(REGIONAL, "Non-UK", f"Which country is the {rank} market by revenue outside the United Kingdom?",
            f"Outside the United Kingdom, which country ranks as the {rank} market by revenue?",
            f"Leaving out the United Kingdom, what is the {rank} country for revenue?",
            f"Outside the United Kingdom, the {rank} market by revenue is {country}.", country)

    top_by_country = sales.groupby(["Country", "Description"])["Quantity"].sum()
    for country in top_countries:
        product = top_by_country.loc[country].idxmax()
        group = "UK" if country == UK else "Non-UK"
        add(REGIONAL, group, f"What is the best-selling product by units in {country}?",
            f"Which product sells the most units in {country}?", f"In {country}, which item is the top seller by quantity?",
            f"The best-selling product in {country} is {product}.", product)

    country_orders = orders[orders["Country"] != "Unspecified"].groupby("Country")["Revenue"].agg(["mean", "size"])
    busy_countries = country_orders[country_orders["size"] >= 30]
    if len(busy_countries):
        big_spender = busy_countries["mean"].idxmax()
        add(REGIONAL, "UK" if big_spender == UK else "Non-UK",
            "Among countries with at least 30 orders, which has the highest average order value?",
            "Which country with 30 or more orders spends the most per order on average?",
            "Looking only at countries with 30 plus orders, where is the average order largest?",
            f"Among countries with at least 30 orders, {big_spender} has the highest average order value.", big_spender)

    # ----- Competitive positioning (product against product) -----
    by_product = sales.groupby("Description")["Revenue"].sum().sort_values(ascending=False)
    top_products = list(by_product.index[:10])
    rank_words = ["top", "second highest", "third highest", "fourth highest", "fifth highest",
                  "sixth highest", "seventh highest", "eighth highest", "ninth highest", "tenth highest"]
    for rank, product in zip(rank_words, top_products):
        add(POSITION, "Global", f"Which product is the {rank} earner by revenue?",
            f"Which product ranks as the {rank} for total revenue?", f"What is the {rank} revenue product in the range?",
            f"The {rank} product by revenue is {product}.", product)
    volume_leader = sales.groupby("Description")["Quantity"].sum().idxmax()
    add(POSITION, "Global", "Which product has sold the most units overall?",
        "What is the best-selling product by total units?", "Across the whole period, which item leads on quantity sold?",
        f"The product with the most units sold overall is {volume_leader}.", volume_leader)
    top10_share = by_product.head(10).sum() / revenue_total
    add(POSITION, "Global", "What share of total revenue comes from the top 10 products?",
        "How much of total revenue do the ten best products generate?", "How concentrated is revenue in the ten leading products?",
        f"The top 10 products generate about {percent(top10_share)} of total revenue.", percent(top10_share))
    # Product against product comparisons. `first` is always the bigger earner.
    # FIX FOR POSITION BIAS: the first version always named the right answer LAST in
    # training and FIRST in testing, so the model learned "pick the last product named"
    # and got all 5 tests wrong. Now the order is shuffled (with a fixed seed, so it is
    # the same every run), and the two training wordings always use OPPOSITE orders.
    order_rng = random.Random(928)
    for first, second in zip(top_products[0:10:2], top_products[1:10:2]):
        q1_pair = (first, second) if order_rng.random() < 0.5 else (second, first)
        q2_pair = (q1_pair[1], q1_pair[0])
        q3_pair = (first, second) if order_rng.random() < 0.5 else (second, first)
        add(POSITION, "Global", f"Which earns more revenue, {q1_pair[0]} or {q1_pair[1]}?",
            f"Between {q2_pair[0]} and {q2_pair[1]}, which product brings in more revenue?",
            f"Comparing {q3_pair[0]} with {q3_pair[1]}, which is the bigger revenue earner?",
            f"The bigger revenue earner of the two is {first}.", first)

    return facts


def load_facts():
    sales, report = clean(load_raw())
    return build_facts(sales, report), sales, report