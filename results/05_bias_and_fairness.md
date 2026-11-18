# Requirements 5-6: Bias assessment and fairness checks

## 1. Data bias: who is represented in the dataset

| Market | Share of sales rows | Share of revenue | Share of customers |
|---|---|---|---|
| United Kingdom | 91.8% | 84.8% | 90.2% |
| Netherlands | 0.4% | 2.9% | 0.2% |
| EIRE | 1.5% | 2.7% | 0.1% |
| Germany | 1.6% | 2.1% | 2.2% |
| France | 1.5% | 1.9% | 2.0% |
| Australia | 0.2% | 1.4% | 0.2% |
| Switzerland | 0.4% | 0.5% | 0.5% |
| Spain | 0.5% | 0.5% | 0.7% |
| All other countries (30) | 2.1% | 3.3% | 3.9% |

| Risk | Evidence | Effect on insights |
|---|---|---|
| Home market dominance | The United Kingdom is 92% of sales rows | Totals and averages mostly describe UK customers |
| Missing customer IDs | 25% of sales rows have no customer ID | Customer behavior findings leave these buyers out |
| Incomplete final month | Data ends on December 09, 2011 | The last month looks weak unless it is treated as partial |
| No demographic fields | Age, gender and income are not recorded | Prompts must not assume who the customers are |
| One company only | All rows come from a single retailer | Findings describe this retailer, not the whole market or its competitors |

## 2. Prompt bias: coverage

| Market research area | Prompts |
|---|---|
| Market trends | 120 |
| Consumer behavior | 96 |
| Regional markets | 96 |
| Competitive positioning | 102 |

| Market the prompt is about | Prompts |
|---|---|
| Global | 276 |
| UK | 18 |
| Non-UK | 120 |

The United Kingdom is 92% of the data rows but 13% of the prompts about a specific market. The prompt set was balanced on purpose so smaller markets are not ignored.

## 3. Prompt bias: leading language

Curated prompts checked: 414. Prompts flagged: 0.

| Biased prompt | Problem | Detector found | Fair rewrite | Rewrite flagged? |
|---|---|---|---|---|
| Explain why the United Kingdom is the best market we have. | Assumes the conclusion and asks for one side only | asks for one side only | Compare the United Kingdom with our other markets on revenue, average order value and repeat orders. | No |
| Obviously overseas customers are less loyal. How do we fix that? | States an untested claim about a group as fact | assumes the answer | What share of customers in each country ordered more than once? | No |
| Which products do women buy as gifts for the home? | Assumes gender, which the dataset does not record | stereotype about a group | Which products sell the most units, and what do we know and not know about who buys them? | No |
| Customers always order more before Christmas. Confirm that our sales follow this. | Absolute wording and asks only for confirmation | asks for one side only, absolute wording | How does monthly revenue change across the year, and which months are highest and lowest? | No |
| What do normal customers spend compared with foreign buyers? | Treats the home market as the norm and others as outsiders | stereotype about a group, home market treated as the norm | What is the average order value in each country? | No |
| Prove that our cheap customers are not worth serving. | Loaded label and one sided request | asks for one side only, stereotype about a group | How is revenue spread across small, medium and large customers? | No |

## 4. Model bias: accuracy by market

| Market | Original model | Fine-tuned model |
|---|---|---|
| Global | 2/46 (4%) | 33/46 (72%) |
| Non-UK | 0/20 (0%) | 17/20 (85%) |
| UK | 0/3 (0%) | 3/3 (100%) |
