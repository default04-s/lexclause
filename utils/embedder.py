import streamlit as st
from sentence_transformers import SentenceTransformer


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("BAAI/bge-small-en")


model = load_embedding_model()

def generate_embeddings(clauses):

    embeddings = model.encode(clauses)

    return embeddings

def generate_query_embedding(query):

    embedding = model.encode(query)

    return embedding