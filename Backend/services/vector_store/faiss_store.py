import json
from pathlib import Path


def create_vector_store(chunks: list[str]) -> None:
    """
    Saves text chunks to a local JSON index for retrieval.

    Args:
        chunks (list[str]): List of text chunks to store.

    Raises:
        ValueError: If chunks list is empty.
    """
    if not chunks:
        raise ValueError("Cannot create vector store with empty chunks.")

    backend_dir = Path(__file__).resolve().parent.parent.parent
    index_path = backend_dir / "faiss_index"
    index_path.mkdir(parents=True, exist_ok=True)

    with open(index_path / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
