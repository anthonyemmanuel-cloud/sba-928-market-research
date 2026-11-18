# Market Research with AI Prompt Engineering

**SBA 928: Enhancing Market Research with AI Prompt Engineering**
Per Scholas AI Prompt Engineering (2026-CAX-255) · Anthony Emmanuel

## What this project does

| Requirement | What the code does | File |
|---|---|---|
| 1. Source a dataset and curate prompts | Loads the public UCI Online Retail dataset, calculates market research facts from it, and builds a prompt for each one across four areas (market trends, consumer behavior, regional markets, competitive positioning) | `data.py`, `prompts.py` |
| 2. Prompt variations | Writes every prompt six ways (direct, role, context, format, audience, paraphrase) | `prompts.py` |
| 3. Fine-tuning experiment | Fine-tunes `google/flan-t5-small` on five of the variations | `finetune.py` |
| 4. Comparison | Tests the original and fine-tuned models on the sixth variation, which neither has seen, and scores accuracy and relevance | `finetune.py` |
| 5. Bias assessment | Measures bias in the data, the prompts and the model's accuracy by market | `bias.py` |
| 6. Fairness strategies | Balanced prompt coverage, a leading-language detector with fair rewrites, and accuracy reported by market | `bias.py` |

Every answer is calculated from the data, so the correct insight for every prompt is known and the models can be scored fairly.

## How to get the dataset

The dataset is the **Online Retail** dataset from the UCI Machine Learning Repository (CC BY 4.0).
Page: https://archive.ics.uci.edu/dataset/352/online+retail

```bash
mkdir -p data
curl -L -o data/online_retail.zip "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
unzip data/online_retail.zip -d data
```

The data files are not stored in this repository because of their size.

## How to install and run

```bash
uv sync
uv run sba-928-market-research --part prompts    # Requirements 1-2
uv run sba-928-market-research --part finetune   # Requirements 3-4 (downloads the model the first time)
uv run sba-928-market-research --part bias       # Requirements 5-6
uv run pytest                                    # 12 automated tests
```

Results are saved as tables in the `results/` folder, and the full prompt dataset is saved as `results/market_research_prompts.csv`.