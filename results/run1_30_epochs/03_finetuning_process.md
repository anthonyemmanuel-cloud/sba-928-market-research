# Requirement 3: The fine-tuning experiment

## Setup

| Setting | Value |
|---|---|
| Model | google/flan-t5-small (77 million parameters) |
| Training examples | 345 prompts (5 techniques for every fact) |
| Test examples | 69 prompts (the paraphrase technique, never seen in training) |
| Epochs | 30 |
| Learning rate | 0.0005 |
| Batch size | 8 |
| Device | cpu |
| Training time | 6.8 minutes |

## Progress during training (tested on the unseen prompts)

| Epoch | Training loss | Test accuracy | Relevance |
|---|---|---|---|
| 10 | 0.032 | 54/69 (78%) | 0.80 |
| 20 | 0.006 | 52/69 (75%) | 0.74 |
| 30 | 0.003 | 49/69 (71%) | 0.73 |
