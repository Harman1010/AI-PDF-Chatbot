Similarity Score Tuning

Embedding Model:
all-MiniLM-L6-v2

Distance Metric:
FAISS L2 Distance

Observations:

Skills Question
1.42
1.47
1.61

Projects Question
1.39
1.52
1.67

Unrelated Question
2.63
2.78
3.01

Chosen Threshold

2.0

Reason

Relevant chunks consistently produced lower L2 distances than unrelated chunks.
The threshold was selected after empirical testing and can be further tuned with a larger evaluation dataset.