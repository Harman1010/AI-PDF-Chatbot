# Retrieval Threshold Analysis

## Embedding Model

- all-MiniLM-L6-v2

## Vector Database

- FAISS

## Similarity Metric

- L2 Distance

## Observations

| Question | Chunk 1 | Chunk 2 | Chunk 3 | Chunk 4 | Chunk 5 | Chunk 6 | Relevant |
|-----------|--------:|--------:|--------:|--------:|--------:|--------:|:--------:|
| What are Harman's skills? | 1.4270 | 1.4755 | 1.6135 | 1.6261 | 1.7911 | 1.8069 | ✅ |
| What are Harman's projects? | 1.3782 | 1.4418 | 1.4887 | 1.5043 | 1.7061 | 1.8476 | ✅ |
| Technologies used by Harman | 1.3460 | 1.5150 | 1.5360 | 1.6331 | 1.6910 | 1.7773 | ✅ |
| Explain FastAPI | 1.3455 | 1.6635 | 1.6750 | 1.7240 | 1.7641 | 1.7712 | ✅ |
| Prime Minister of Japan | 1.8407 | 1.8736 | 1.8933 | 1.9010 | 1.9453 | 2.0309 | ❌ |

---

## Conclusion

- Relevant document questions consistently produced lower L2 distances.
- Unrelated questions produced noticeably larger distances.
- An empirical threshold of **1.82** was selected after evaluating representative queries.
- This threshold is treated as a tunable hyperparameter and can be re-evaluated for different embedding models or datasets.