# Requirement 3: The fine-tuning experiment

## Setup

| Setting | Value |
|---|---|
| Model | google/flan-t5-small (77 million parameters) |
| Training examples | 345 prompts (5 techniques for every fact) |
| Test examples | 69 prompts (the paraphrase technique, never seen in training) |
| Epochs | 10 |
| Learning rate | 0.0005 |
| Batch size | 8 |
| Device | cpu |
| Training time | 2.4 minutes |

## Progress during training (tested on the unseen prompts)

| Epoch | Training loss | Test accuracy | Relevance |
|---|---|---|---|
| 2 | 0.484 | 16/69 (23%) | 0.52 |
| 4 | 0.180 | 25/69 (36%) | 0.60 |
| 6 | 0.109 | 32/69 (46%) | 0.62 |
| 8 | 0.058 | 45/69 (65%) | 0.75 |
| 10 | 0.045 | 53/69 (77%) | 0.76 |
