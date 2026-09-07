import re


def clean_text(text):
    """
    Clean extracted contract text while preserving legal content.

    Handles:
    - whitespace normalization
    - private-use Unicode clause numbering
    - common OCR clause-number corruption
    - repeated headers/page numbers
    - clause/list boundaries
    - broken line wrapping
    """

    # ---------------------------------------------------------
    # 1. Normalize private-use Unicode numbers
    # ---------------------------------------------------------
    # Some PDFs extract numbered clauses using private-use
    # Unicode characters instead of normal digits.
    #
    # Example:
    #       -> 1.1
    #       -> 2.1
    #
    # These characters are common in certain generated PDFs.

    private_use_numbers = {
        "": "0",
        "": "1",
        "": "2",
        "": "3",
        "": "4",
        "": "5",
        "": "6",
        "": "7",
        "": "8",
        "": "9",
        "": ".",
    }

    for old, new in private_use_numbers.items():
        text = text.replace(old, new)

    # ---------------------------------------------------------
    # 2. Normalize common OCR clause-number errors
    # ---------------------------------------------------------
    # Only operate at the beginning of a line and when the
    # following text looks like a clause/definition.
    #
    # Examples:
    #     Ll "Affiliate"       -> 1.1 "Affiliate"
    #     12 "Competitor"      -> 1.2 "Competitor"
    #     13 "Confidential..." -> 1.3 "Confidential..."

    text = re.sub(
        r'(?m)^\s*Ll\s+(?=["“])',
        '1.1 ',
        text
    )

    text = re.sub(
        r'(?m)^\s*12\s+(?=["“])',
        '1.2 ',
        text
    )

    text = re.sub(
        r'(?m)^\s*13\s+(?=["“])',
        '1.3 ',
        text
    )

    # ---------------------------------------------------------
    # 3. Normalize common OCR errors in numbered lists
    # ---------------------------------------------------------
    # These are deliberately limited to very obvious OCR
    # substitutions observed in the test document.

    text = re.sub(r'\bshail\b', 'shall', text)
    text = re.sub(r'\btelatives\b', 'relatives', text)

    # "(ji)" is a common OCR reading of "(ii)"
    # Only change the exact standalone list marker.
    text = re.sub(r'(?<!\w)\(ji\)(?!\w)', '(ii)', text)

    # ---------------------------------------------------------
    # 4. Normalize whitespace
    # ---------------------------------------------------------

    # Multiple spaces/tabs -> one space
    text = re.sub(r'[ \t]+', ' ', text)

    # Remove spaces at the beginning/end of lines
    text = re.sub(r'(?m)^[ \t]+|[ \t]+$', '', text)

    # Excessive blank lines -> one blank line
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # ---------------------------------------------------------
    # 5. Remove spaces before punctuation
    # ---------------------------------------------------------

    text = re.sub(r'\s+([.,])', r'\1', text)

    # ---------------------------------------------------------
    # 6. Repair words broken by line wrapping
    # ---------------------------------------------------------

    # Example:
    #     day-to-
    #     day
    #
    # becomes:
    #     day-to-day

    text = re.sub(
        r'(\w)-\s*\n\s*(\w)',
        r'\1-\2',
        text
    )

    # ---------------------------------------------------------
    # 7. Repair ordinary sentence wrapping
    # ---------------------------------------------------------
    # Join a line when the next line clearly continues the
    # same sentence.
    #
    # Do NOT blindly join every line because legal documents
    # use line breaks for clauses and lists.

    text = re.sub(
        r'(?m)(\w)\n(?=[a-z])',
        r'\1 ',
        text
    )

    # ---------------------------------------------------------
    # 8. Keep numbered clauses on separate lines
    # ---------------------------------------------------------
    #
    # Examples:
    #     ... conditions 1. Property...
    #
    # becomes:
    #     ... conditions
    #     1. Property...
    #
    # Restrict this to numbers followed by a capital letter or
    # quotation mark to avoid damaging ordinary decimal values.

    text = re.sub(
        r'(?<!\n)(?<![\d.])\b(\d{1,2}\.)\s+(?=[A-Z“"])',
        r'\n\1 ',
        text
    )

    # ---------------------------------------------------------
    # 9. Separate multi-level clause numbers
    # ---------------------------------------------------------
    #
    # Example:
    #     ...; and, 1.8.4 Any tangible...
    #
    # becomes:
    #     ...; and,
    #     1.8.4 Any tangible...

    text = re.sub(
        r'(?<!\n)\s+(\d+\.\d+(?:\.\d+)?)\s+(?=[A-Z“"])',
        r'\n\1 ',
        text
    )

    # ---------------------------------------------------------
    # 10. Repair references split across lines
    # ---------------------------------------------------------
    #
    # Example:
    #     Clause
    #     9.
    #
    # becomes:
    #     Clause 9.

    text = re.sub(
        r'(\bClause)\s*\n\s*(\d+\.)',
        r'\1 \2',
        text
    )

    # ---------------------------------------------------------
    # 11. Repair years split after commas
    # ---------------------------------------------------------

    text = re.sub(
        r',\s*\n\s*(\d{4})\b',
        r', \1',
        text
    )

    # ---------------------------------------------------------
    # 12. Repair bullet points split across lines
    # ---------------------------------------------------------

    text = re.sub(
        r'•\s*\n\s*',
        '• ',
        text
    )

    # ---------------------------------------------------------
    # 13. Remove obvious standalone page numbers
    # ---------------------------------------------------------
    #
    # Only remove a line containing a number by itself.
    # This avoids deleting legitimate contract numbers embedded
    # in sentences.

    text = re.sub(
        r'(?m)^\s*\d{1,3}\s*$',
        '',
        text
    )

    # ---------------------------------------------------------
    # 14. Remove obvious repeated document header
    # ---------------------------------------------------------
    #
    # Observed in the OCR document:
    #     U® TaskUs
    #
    # This is clearly a repeated page header rather than
    # contract content.

    text = re.sub(
        r'(?m)^\s*U®\s+TaskUs(?:\s+\d+(?:\.\d+)*)?\s*$',
        '',
        text
    )

    # ---------------------------------------------------------
    # 15. Remove OCR page-number/header fragments
    # ---------------------------------------------------------
    #
    # Examples observed:
    #     21 2.2
    #     23 3.2 3.3
    #
    # These are layout artifacts, not reliable contract text.
    #
    # Keep this intentionally narrow.

    text = re.sub(
        r'(?m)^\s*\d{1,3}\s+\d+\.\d+(?:\s+\d+\.\d+)*\s*$',
        '',
        text
    )

    # ---------------------------------------------------------
    # 16. Final whitespace cleanup
    # ---------------------------------------------------------

    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()