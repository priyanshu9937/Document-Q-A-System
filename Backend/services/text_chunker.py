from typing import List

def split_text(text: str) -> List[str]:
    """
    Splits text into smaller chunks using a simple character-based chunking approach.

    Args:
        text (str): The full input text.

    Returns:
        List[str]: A list of text chunks.
    """
    if not text or not text.strip():
        return []

    text = text.strip()
    chunk_size = 500
    chunk_overlap = 100

    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start += chunk_size - chunk_overlap

    return chunks
