from utils.cleaner import clean_text
from utils.legal_segmenter import segment_legal_sections
from utils.embedder import generate_embeddings
from utils.vectordb import store_legal_sections

legal_path = "data/legal_knowledge.txt"

print("\nStarting legal knowledge ingestion...\n")

# Load legal text
with open(legal_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# Clean text
cleaned_text = clean_text(raw_text)

# Segment legal sections
sections = segment_legal_sections(cleaned_text)

print(f"Total legal sections found: {len(sections)}")

# Generate embeddings
embeddings = generate_embeddings(sections)

print("Legal embeddings generated successfully.")

# Store in ChromaDB
store_legal_sections(sections, embeddings)

print("Legal sections stored successfully.")