import re

# Extract contract clause numbers
def extract_clause_titles(clauses):

    titles = []

    for clause in clauses:

        match = re.search(r'(\d+\.\s.*?Clause)', clause)

        if match:
            titles.append(match.group(1))

    return titles

# Extract legal section titles
def extract_legal_titles(sections):

    titles = []

    for section in sections:

        match = re.search(
            r'(SECTION\s+\d+\s+OF\s+THE\s+INDIAN\s+CONTRACT\s+ACT,\s+1872)',
            section,
            re.IGNORECASE
        )

        if match:
            titles.append(match.group(1))

    return titles