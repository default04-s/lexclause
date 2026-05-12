import chromadb

# Persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_storage")

# Contract clause collection
contract_collection = client.get_or_create_collection(
    name="rental_agreement"
)

# Legal knowledge collection
legal_collection = client.get_or_create_collection(
    name="legal_knowledge"
)

# Store rental agreement clauses
def store_clauses(clauses, embeddings):

    for i, (clause, embedding) in enumerate(zip(clauses, embeddings)):

        contract_collection.add(
            documents=[clause],
            embeddings=[embedding.tolist()],
            ids=[f"contract_clause_{i+1}"]
        )

# Store legal sections
def store_legal_sections(sections, embeddings):

    for i, (section, embedding) in enumerate(zip(sections, embeddings)):

        legal_collection.add(
            documents=[section],
            embeddings=[embedding.tolist()],
            ids=[f"legal_section_{i+1}"]
        )

# Search rental clauses
def search_clauses(query_embedding):

    results = contract_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=3
    )

    return results

# Search legal sections
def search_legal_sections(query_embedding):

    results = legal_collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=2
    )

    return results