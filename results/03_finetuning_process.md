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
| Training time | 2.3 minutes |

## Progress during training (tested on the unseen prompts)

| Epoch | Training loss | Test accuracy | Relevance |
|---|---|---|---|
| 2 | 0.479 | 12/69 (17%) | 0.51 |
| 4 | 0.186 | 18/69 (26%) | 0.60 |
| 6 | 0.110 | 29/69 (42%) | 0.67 |
| 8 | 0.067 | 52/69 (75%) | 0.80 |
| 10 | 0.032 | 54/69 (78%) | 0.80 |
