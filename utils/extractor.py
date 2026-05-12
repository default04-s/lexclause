import fitz

def extract_text_from_pdf(pdf_path):

    doc = fitz.open(pdf_path)

    full_text = ""

    for page in doc:
        text = page.get_text()
        full_text += text + "\n"

    return full_text