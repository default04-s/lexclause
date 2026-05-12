from utils.extractor import extract_text_from_pdf
from utils.cleaner import clean_text
from utils.segmenter import segment_clauses
from utils.embedder import generate_embeddings
from utils.vectordb import store_clauses

pdf_path = "data/rental_agreement.pdf"

print("\nStarting document ingestion...\n")

# Extract text
raw_text = extract_text_from_pdf(pdf_path)

# Clean extracted text
cleaned_text = clean_text(raw_text)

# Segment clauses
clauses = segment_clauses(cleaned_text)

print(f"Total clauses found: {len(clauses)}")

# Generate embeddings
embeddings = generate_embeddings(clauses)

print("Embeddings generated successfully.")

# Store in ChromaDB
store_clauses(clauses, embeddings)

print("Clauses stored successfully in ChromaDB.")