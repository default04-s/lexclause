from utils.reranker import rerank_results

documents = [
    "Clause 12. Termination: Either party may terminate employment by giving thirty days' notice.",
    "Clause 6. Compensation: The employee shall receive an annual salary of INR 8,40,000.",
    "Clause 8. Confidentiality: The employee shall not disclose confidential information.",
    "Clause 11. Non-Solicitation: The employee shall not solicit clients after termination.",
    "Clause 3. Probation: The first six months shall constitute the probation period."
]

query = "What causes termination of employment?"

ranked = rerank_results(query, documents, top_k=3)

print("\nTop 3 reranked clauses:\n")

for i, doc in enumerate(ranked, start=1):
    print(f"{i}. {doc}\n")