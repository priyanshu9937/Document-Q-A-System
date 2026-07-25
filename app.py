import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "Backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from services import (
    extract_text_from_pdf,
    split_text,
    create_vector_store,
    retrieve_chunks,
    ask_llm,
)

st.set_page_config(page_title="Document Q&A", page_icon="📄", layout="centered")
st.title("📄 Document Q&A with Streamlit")
st.write("Upload a PDF, index it locally, and ask questions about it.")

UPLOAD_DIR = BACKEND_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR = BACKEND_DIR / "faiss_index"
INDEX_DIR.mkdir(parents=True, exist_ok=True)

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    file_path = UPLOAD_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        text = extract_text_from_pdf(file_path)
        chunks = split_text(text)
        create_vector_store(chunks)
        st.success(f"Indexed '{uploaded_file.name}' with {len(chunks)} chunks.")
    except Exception as exc:
        st.error(f"Failed to process the PDF: {exc}")

question = st.text_input("Ask a question about the document")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    elif not (INDEX_DIR / "chunks.json").exists():
        st.warning("Please upload and index a PDF first.")
    else:
        try:
            docs = retrieve_chunks(question)
            answer = ask_llm(question, docs)

            st.subheader("Answer")
            st.write(answer)

            if docs:
                with st.expander("Retrieved context"):
                    for index, doc in enumerate(docs, start=1):
                        st.write(f"**Chunk {index}**")
                        st.write(doc.page_content[:1200])
        except Exception as exc:
            st.error(f"Could not answer the question: {exc}")
