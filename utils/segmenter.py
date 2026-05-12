import re

def segment_clauses(text):

    # Pattern for numbered clauses
    pattern = r'(\d{1,2}\.\s.*?Clause)'

    matches = list(re.finditer(pattern, text))

    # Capture content before first clause as metadata
    first_clause_start = matches[0].start()

    metadata = text[:first_clause_start].strip()

    clauses = []

    if metadata:
        clauses.append(metadata)

    for i in range(len(matches)):

        start = matches[i].start()

        # If not last clause,
        # end at next clause start
        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        clause = text[start:end].strip()

        clauses.append(clause)

    return clauses