import chromadb

# Persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_storage")


# ===== CHANGED =====
# Returns (or creates) the contract collection requested.
# Example:
# employment_agreement
# rental_agreement
# nda_agreement
# service_agreement
def get_contract_collection(collection_name):
    return client.get_or_create_collection(
        name=collection_name
    )


# Legal knowledge collection (unchanged)
legal_collection = client.get_or_create_collection(
    name="legal_knowledge"
)


# ===== CHANGED =====
# Store clauses in the selected contract collection.
def store_clauses(clauses, embeddings, collection_name):

    contract_collection = get_contract_collection(collection_name)

    for i, (clause, embedding) in enumerate(zip(clauses, embeddings)):

        contract_collection.add(
            documents=[clause],
            embeddings=[embedding.tolist()],
            ids=[f"contract_clause_{i+1}"]
        )


# Store legal sections (unchanged)
def store_legal_sections(sections, embeddings):

    for i, (section, embedding) in enumerate(zip(sections, embeddings)):

        legal_collection.add(
            documents=[section],
            embeddings=[embedding.tolist()],
            ids=[f"legal_section_{i+1}"]
        )


# ===== CHANGED =====
# Search only within the selected contract collection.
def search_clauses(query_embedding, collection_name):

    contract_collection = get_contract_collection(collection_name)

    results = contract_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3
    )

    return results


# Search legal sections (unchanged)
def search_legal_sections(query_embedding):

    results = legal_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

    return results