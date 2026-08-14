import re


# ---------------------------------------------------
# Extract contract clause titles
# ---------------------------------------------------

def extract_clause_titles(clauses):

    titles = []

    for i, clause in enumerate(clauses, start=1):

        # Match: Clause 12. Termination
        match = re.search(
            r"(Clause\s+\d+[.:]?\s*[^\n]*)",
            clause,
            re.IGNORECASE
        )

        if match:
            titles.append(match.group(1).strip())
            continue

        # Match: 12. Termination
        match = re.search(
            r"(^\d+\.\s*[^\n]*)",
            clause,
            re.MULTILINE
        )

        if match:
            titles.append(match.group(1).strip())
            continue

        # Fallback
        titles.append(f"Clause {i}")


    return titles


# ---------------------------------------------------
# Extract legal section titles
# ---------------------------------------------------

def extract_legal_titles(sections):

    titles = []

    for i, section in enumerate(sections, start=1):

        match = re.search(
            r"(SECTION\s+\d+\s+OF\s+THE\s+INDIAN\s+CONTRACT\s+ACT,\s*1872)",
            section,
            re.IGNORECASE
        )

        if match:
            titles.append(match.group(1).strip())
            continue

        match = re.search(
            r"(Section\s+\d+)",
            section,
            re.IGNORECASE
        )

        if match:
            titles.append(match.group(1).strip())
            continue

        titles.append(f"Section {i}")

    return titles