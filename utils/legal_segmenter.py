import re

def segment_legal_sections(text):

    pattern = r'(SECTION\s+\d+.*?)(?=SECTION\s+\d+|$)'

    sections = re.findall(pattern, text, re.DOTALL)

    cleaned_sections = [section.strip() for section in sections]

    return cleaned_sections