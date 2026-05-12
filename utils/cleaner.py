import re

def clean_text(text):

    # Replace multiple spaces/tabs with a single space
    # Preserves line breaks while removing messy spacing
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove excessive empty lines
    # Keeps document structure readable
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Remove unwanted spaces before punctuation
    # Example: "word ." -> "word."
    text = re.sub(r'\s+([.,])', r'\1', text)

    # Ensure numbered clauses start on a new line
    # Example: "...conditions: 1. Property..." -> new line before 1.
    text = re.sub(r'(?<!\n)(?<!\d)(\d{1,2}\.\s)', r'\n\1', text)

    # Fix broken clause references caused by PDF extraction
    # Example: "Clause \n9." -> "Clause 9."
    text = re.sub(r'(\w)\s*\n\s*(\d+\.)', r'\1 \2', text)

    # Fix broken year/number formatting
    # Example: "Act,\n1872" -> "Act, 1872"
    text = re.sub(r',\s*\n\s*(\d+)', r', \1', text)

    # Fix bullet points split across lines
    # Example: "•\nrepeatedly fails" -> "• repeatedly fails"
    text = re.sub(r'•\s*\n\s*', '• ', text)

    # Repair words broken by PDF line wrapping
    # Example: "day-to-\nday" -> "day-to-day"
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1-\2', text)

    return text.strip()


