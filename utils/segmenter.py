import re

def segment_clauses(text):

    # ===== CHANGED =====
    # Detect numbered clause headings.
    pattern = r'^\d{1,2}\.\s+.*$'

    # ===== CHANGED =====
    # Search across multiple lines.
    matches = list(re.finditer(pattern, text, re.MULTILINE))

    # ===== CHANGED =====
    # If no numbered clauses are found, return the whole document.
    if not matches:
        return [text.strip()]

    # Capture content before first clause as metadata
    first_clause_start = matches[0].start()

    metadata = text[:first_clause_start].strip()

    clauses = []

    if metadata:
        clauses.append(metadata)

    for i in range(len(matches)):

        start = matches[i].start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        clause = text[start:end].strip()

        clauses.append(clause)

    return clauses