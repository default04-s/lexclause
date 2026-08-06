from sentence_transformers import CrossEncoder

# Load the reranker model once
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_results(query, retrieved_documents, top_k=3):
    """
    Reranks retrieved documents using a CrossEncoder.

    Args:
        query (str): User's question.
        retrieved_documents (list): Documents retrieved from ChromaDB.
        top_k (int): Number of top documents to return.

    Returns:
        list: Top-k reranked documents.
    """

    # Create (query, document) pairs
    pairs = [(query, doc) for doc in retrieved_documents]

    # Predict relevance scores
    scores = reranker.predict(pairs)

    # Pair each document with its score
    ranked = list(zip(retrieved_documents, scores))

    # Sort by descending score
    ranked.sort(key=lambda x: x[1], reverse=True)

    # Return only the documents
    return [doc for doc, _ in ranked[:top_k]]