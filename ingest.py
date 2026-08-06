from utils.extractor import extract_text
from utils.cleaner import clean_text
from utils.segmenter import segment_clauses
from utils.embedder import generate_embeddings
from utils.vectordb import store_clauses

# ===== CHANGED =====
# List of contracts to ingest.
contracts = {
    "employment_contract": "data/employment_contract.txt",
    "rental_contract": "data/rental_contract.txt",
    "nda_contract": "data/nda_contract.txt",
    "service_contract": "data/service_contract.txt"
}

# ===== CHANGED =====
# Ingest each contract into its own ChromaDB collection.
for collection_name, contract_path in contracts.items():

    print(f"\nStarting ingestion for '{collection_name}'...\n")

    # Extract text
    raw_text = extract_text(contract_path)

    # Clean extracted text
    cleaned_text = clean_text(raw_text)

    # Segment clauses
    clauses = segment_clauses(cleaned_text)

    print(f"Total clauses found: {len(clauses)}")

    # Generate embeddings
    embeddings = generate_embeddings(clauses)

    print("Embeddings generated successfully.")

    # ===== CHANGED =====
    # Store clauses in the corresponding ChromaDB collection.
    store_clauses(clauses, embeddings, collection_name)

    print(f"Clauses stored successfully in '{collection_name}'.")

print("\nAll contracts have been ingested successfully.")