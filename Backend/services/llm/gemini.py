import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Load .env correctly
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
if not os.getenv("GEMINI_API_KEY"):
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")


def ask_llm(question: str, docs: List) -> str:
    """
    Returns a local fallback answer based on retrieved chunks.

    Args:
        question (str): The question to answer.
        docs (List): List of Document-like objects containing context.

    Returns:
        str: A simple fallback response describing the matched document content.

    Raises:
        ValueError: If the question or docs are empty.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not docs:
        raise ValueError("No document chunks were found for the question.")

    top_content = docs[0].page_content.strip()
    if not top_content:
        raise ValueError("Retrieved document chunks contain no text.")

    return (
        "Local fallback mode is active. "
        "Here is the most relevant document fragment matched for your question:\n\n"
        f"{top_content[:1200]}"
    )
