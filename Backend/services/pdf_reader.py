import fitz  # PyMuPDF
from pathlib import Path

def extract_text_from_pdf(file_path: Path) -> str:
    """
    Extracts all text from a PDF file page by page using PyMuPDF.

    Args:
        file_path (Path): Path to the PDF file.

    Returns:
        str: The complete extracted text from the PDF.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the PDF is corrupted, has no pages, or contains no extractable text.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file. It may be corrupted or invalid. Error: {str(e)}")

    try:
        if len(doc) == 0:
            raise ValueError("The PDF document contains 0 pages.")

        extracted_pages = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            page_text = page.get_text()
            if page_text.strip():
                extracted_pages.append(page_text)

        full_text = "\n".join(extracted_pages).strip()

        if not full_text:
            raise ValueError("No text could be extracted from the PDF. It might be empty or scanned images.")

        return full_text
    finally:
        doc.close()
