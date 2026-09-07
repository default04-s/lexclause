from utils.extractor import extract_text
from utils.cleaner import clean_text
from utils.segmenter import segment_clauses

from utils.embedder import generate_embeddings
from utils.vectordb import (
    clear_contract_collection,
    store_clauses
)


# ---------------------------------------------------
# INGEST ONE CONTRACT
# ---------------------------------------------------

def ingest_contract(file_path):
    """
    Process and store one uploaded contract.

    Pipeline:
        Extract
        -> Clean
        -> Segment
        -> Embed
        -> Replace current contract
        -> Store
    """

    print("\nStarting contract ingestion...\n")

    # ---------------------------------------------------
    # 1. EXTRACT TEXT
    # ---------------------------------------------------

    print("Extracting text...")

    raw_text = extract_text(file_path)

    if not raw_text.strip():
        raise ValueError(
            "No text could be extracted from the document."
        )

    print(
        f"Raw text extracted: {len(raw_text)} characters"
    )

    # ---------------------------------------------------
    # 2. CLEAN TEXT
    # ---------------------------------------------------

    print("Cleaning text...")

    cleaned_text = clean_text(raw_text)

    if not cleaned_text.strip():
        raise ValueError(
            "Cleaning produced empty text."
        )

    print(
        f"Cleaned text: {len(cleaned_text)} characters"
    )

    # ---------------------------------------------------
    # 3. SEGMENT CLAUSES
    # ---------------------------------------------------

    print("Segmenting document...")

    segments = segment_clauses(cleaned_text)

    if not segments:
        raise ValueError(
            "No document segments were produced."
        )

    print(
        f"Total segments found: {len(segments)}"
    )

    # ---------------------------------------------------
    # 4. EXTRACT EMBEDDABLE TEXT
    # ---------------------------------------------------

    clause_texts = []

    for segment in segments:

        # New segmenter returns structured dictionaries.
        if isinstance(segment, dict):

            segment_type = segment.get("type")

            # Only embed meaningful contract content.
            if segment_type in {
                "clause",
                "section",
                "annexure",
                "schedule"
            }:

                text = segment.get("text", "").strip()

                if text:
                    clause_texts.append(text)

        # Backward compatibility if segmenter returns strings.
        elif isinstance(segment, str):

            text = segment.strip()

            if text:
                clause_texts.append(text)

    if not clause_texts:
        raise ValueError(
            "No embeddable contract clauses were found."
        )

    print(
        f"Embeddable clauses: {len(clause_texts)}"
    )

    # ---------------------------------------------------
    # 5. GENERATE EMBEDDINGS
    # ---------------------------------------------------

    print("Generating embeddings...")

    embeddings = generate_embeddings(
        clause_texts
    )

    print("Embeddings generated successfully.")

    # ---------------------------------------------------
    # 6. REPLACE CURRENT CONTRACT
    # ---------------------------------------------------

    print("Replacing current contract...")

    clear_contract_collection()

    store_clauses(
        clause_texts,
        embeddings
    )

    print(
        "Contract clauses stored in 'current_contract'."
    )

    print(
        "\nContract ingestion completed successfully."
    )

    # Return structured segments for the frontend.
    return segments


# ---------------------------------------------------
# DIRECT EXECUTION
# ---------------------------------------------------

if __name__ == "__main__":

    print(
        "This module is intended to ingest an uploaded "
        "contract through the application."
    )