from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query,docs,top_n=3):
    pairs = []
    for doc in docs:
        pairs.append([query,doc.page_content])
    scores = reranker.predict(pairs)
    ranked = sorted(zip(docs,scores),
        key=lambda x:x[1],reverse=True)
    return [
        doc for doc,score in ranked[:top_n]
    ]