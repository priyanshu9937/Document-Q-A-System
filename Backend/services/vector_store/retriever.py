import json
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Document:
    page_content: str


def retrieve_chunks(question: str) -> list[Document]:
    """
    Loads local chunks from the JSON index and returns the best-matching chunks.

    Args:
        question (str): The search query or question.

    Returns:
        list[Document]: A list of Document objects containing matched chunks.

    Raises:
        ValueError: If the question is empty.
        FileNotFoundError: If the local chunk index does not exist.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    backend_dir = Path(__file__).resolve().parent.parent.parent
    index_path = backend_dir / "faiss_index"
    chunks_file = index_path / "chunks.json"

    if not chunks_file.exists():
        raise FileNotFoundError("Chunk index not found. Please upload a PDF first to initialize the index.")

    with open(chunks_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not isinstance(chunks, list) or not chunks:
        raise ValueError("Stored chunk data is invalid or empty.")

    query_words = set(re.findall(r"\w+", question.lower()))

    scored_chunks = []
    for chunk in chunks:
        chunk_words = set(re.findall(r"\w+", str(chunk).lower()))
        score = len(query_words & chunk_words)
        scored_chunks.append((score, str(chunk)))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    top_chunks = [Document(page_content=chunk) for score, chunk in scored_chunks if score > 0][:3]

    if not top_chunks:
        top_chunks = [Document(page_content=chunk) for _, chunk in scored_chunks[:3]]

    return top_chunks
