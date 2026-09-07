import chromadb


# ---------------------------------------------------
# PERSISTENT CHROMADB CLIENT
# ---------------------------------------------------

client = chromadb.PersistentClient(
    path="chroma_storage"
)


# ---------------------------------------------------
# COLLECTION NAMES
# ---------------------------------------------------

CONTRACT_COLLECTION = "current_contract"
LEGAL_COLLECTION = "legal_knowledge"


# ---------------------------------------------------
# CURRENT CONTRACT COLLECTION
# ---------------------------------------------------

def get_contract_collection():
    """
    Return the collection containing the currently
    uploaded contract.
    """

    return client.get_or_create_collection(
        name=CONTRACT_COLLECTION
    )


# ---------------------------------------------------
# LEGAL KNOWLEDGE COLLECTION
# ---------------------------------------------------

def get_legal_collection():
    """
    Return the permanent Indian Contract Act
    knowledge collection.
    """

    return client.get_or_create_collection(
        name=LEGAL_COLLECTION
    )


# ---------------------------------------------------
# COLLECTION CHECK
# ---------------------------------------------------

def collection_has_data(collection_name):
    """
    Check whether a ChromaDB collection exists
    and contains documents.
    """

    try:
        collection = client.get_collection(
            name=collection_name
        )

        return collection.count() > 0

    except Exception:
        return False


# ---------------------------------------------------
# CLEAR CURRENT CONTRACT
# ---------------------------------------------------

def clear_contract_collection():
    """
    Remove all clauses from the current contract
    collection.

    This is called before ingesting a new document so
    clauses from a previous contract cannot contaminate
    retrieval for the new document.
    """

    try:
        client.delete_collection(
            name=CONTRACT_COLLECTION
        )

    except Exception:
        pass


# ---------------------------------------------------
# STORE CONTRACT CLAUSES
# ---------------------------------------------------

def store_clauses(clauses, embeddings):
    """
    Store clauses belonging to the currently uploaded
    contract.

    Each clause receives a unique ID.
    """

    contract_collection = get_contract_collection()

    documents = []
    vectors = []
    ids = []

    for i, (clause, embedding) in enumerate(
        zip(clauses, embeddings),
        start=1
    ):

        documents.append(clause)

        vectors.append(
            embedding.tolist()
        )

        ids.append(
            f"contract_clause_{i}"
        )

    if documents:

        contract_collection.add(
            documents=documents,
            embeddings=vectors,
            ids=ids
        )


# ---------------------------------------------------
# STORE LEGAL SECTIONS
# ---------------------------------------------------

def store_legal_sections(sections, embeddings):
    """
    Store Indian Contract Act sections in the
    permanent legal knowledge collection.
    """

    legal_collection = get_legal_collection()

    documents = []
    vectors = []
    ids = []

    for i, (section, embedding) in enumerate(
        zip(sections, embeddings),
        start=1
    ):

        documents.append(section)

        vectors.append(
            embedding.tolist()
        )

        ids.append(
            f"legal_section_{i}"
        )

    if documents:

        legal_collection.add(
            documents=documents,
            embeddings=vectors,
            ids=ids
        )


# ---------------------------------------------------
# SEARCH CONTRACT CLAUSES
# ---------------------------------------------------

def search_clauses(query_embedding, n_results=5):
    """
    Search only within the currently uploaded contract.
    """

    contract_collection = get_contract_collection()

    results = contract_collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )

    return results


# ---------------------------------------------------
# SEARCH LEGAL SECTIONS
# ---------------------------------------------------

def search_legal_sections(query_embedding, n_results=5):
    """
    Search the permanent Indian Contract Act
    knowledge collection.
    """

    legal_collection = get_legal_collection()

    results = legal_collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=n_results
    )

    return results