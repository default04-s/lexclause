import chromadb

# Persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_storage")


# ===== CHANGED =====
# Returns (or creates) the contract collection requested.
# Example:
# employment_contract
# rental_contract
# nda_contract
# service_contract
def get_contract_collection(collection_name):
    return client.get_or_create_collection(
        name=collection_name
    )


# Legal knowledge collection
legal_collection = client.get_or_create_collection(
    name="legal_knowledge"
)


# ===== CHANGED =====
# Checks whether a collection exists and contains documents.
def collection_has_data(collection_name):

    try:
        collection = client.get_collection(name=collection_name)
        return collection.count() > 0
    except:
        return False


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


# Store legal sections
def store_legal_sections(sections, embeddings):

    for i, (section, embedding) in enumerate(zip(sections, embeddings), start=1):

        legal_collection.add(
            documents=[section],
            embeddings=[embedding.tolist()],
            ids=[f"legal_section_{i}"]
        )


# ===== CHANGED =====
# Search only within the selected contract collection.
def search_clauses(query_embedding, collection_name):

    contract_collection = get_contract_collection(collection_name)

    results = contract_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=5
    )

    return results


# Search legal sections
def search_legal_sections(query_embedding):

    results = legal_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=5
    )

    return results