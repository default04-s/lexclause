from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("BAAI/bge-small-en")

def generate_embeddings(clauses):

    embeddings = model.encode(clauses)

    return embeddings

def generate_query_embedding(query):

    embedding = model.encode(query)

    return embedding