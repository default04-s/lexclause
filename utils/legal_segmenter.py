import re

def segment_legal_sections(text):

    # ===== CHANGED =====
    # Split the document into contract-specific blocks.
    contract_pattern = (
        r'(Employment Agreement|Residential Rental Agreement|'
        r'Mutual Non-Disclosure Agreement \(NDA\)|Service Agreement)'
        r'(.*?)(?=(Employment Agreement|Residential Rental Agreement|'
        r'Mutual Non-Disclosure Agreement \(NDA\)|Service Agreement|$))'
    )

    contract_blocks = re.findall(contract_pattern, text, re.DOTALL)

    sections = []

    # ===== CHANGED =====
    # Prefix every legal section with its corresponding contract heading.
    for contract_name, contract_text, _ in contract_blocks:

        section_pattern = r'(SECTION\s+\d+.*?)(?=SECTION\s+\d+|$)'

        contract_sections = re.findall(section_pattern, contract_text, re.DOTALL)

        for section in contract_sections:
            sections.append(f"CONTRACT TYPE: {contract_name}\n\n{section.strip()}")

    return sections