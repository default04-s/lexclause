import os
import re
import fitz  # PyMuPDF
from docx import Document
import pytesseract
from PIL import Image


def extract_text(file_path):
    """Extract text from PDF or DOCX."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf(file_path)

    if extension == ".docx":
        return extract_docx(file_path)

    raise ValueError(f"Unsupported file type: {extension}")


def extract_pdf(file_path):
    """Try PyMuPDF first, then OCR if needed."""

    document = fitz.open(file_path)
    pages = []

    for page in document:
        pages.append(page.get_text("text"))

    document.close()

    text = "\n".join(pages).strip()

    if is_extraction_good(text):
        print("Extraction method: PyMuPDF")
        return text

    print("PyMuPDF extraction was poor.")
    print("Extraction method: Tesseract OCR")

    return extract_pdf_with_ocr(file_path)


def extract_pdf_with_ocr(file_path):
    """Extract PDF text using Tesseract."""

    document = fitz.open(file_path)
    pages = []

    for page_number, page in enumerate(document):
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        image = Image.frombytes(
            "RGB",
            [pixmap.width, pixmap.height],
            pixmap.samples
        )

        text = pytesseract.image_to_string(image)
        pages.append(text)

        print(f"OCR: page {page_number + 1}")

    document.close()

    return "\n".join(pages).strip()


def extract_docx(file_path):
    """Extract text from DOCX paragraphs."""

    document = Document(file_path)
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    print("Extraction method: python-docx")

    return "\n".join(paragraphs).strip()


def is_extraction_good(text):
    """Check whether extracted PDF text is usable."""

    if not text:
        return False

    compact_text = re.sub(r"\s+", "", text)

    if len(compact_text) < 100:
        return False

    letters = sum(char.isalpha() for char in compact_text)
    letter_ratio = letters / len(compact_text)

    if letter_ratio < 0.50:
        return False

    replacement_count = text.count("�")

    if replacement_count > 5:
        return False

    words = re.findall(r"\b[A-Za-z]{2,}\b", text)

    if len(words) < 20:
        return False

    return True