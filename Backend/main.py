import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure the Backend directory is in sys.path to prevent import errors
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from services import (
    extract_text_from_pdf,
    split_text,
    create_vector_store,
    retrieve_chunks,
    ask_llm
)

# Load .env correctly using BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
# Fallback to local Backend/.env if not loaded from workspace root
if not os.getenv("GEMINI_API_KEY"):
    load_dotenv(backend_dir / ".env")

# Initialize FastAPI App
app = FastAPI(
    title="Document Q&A System API",
    description="A production-ready RAG application using FastAPI, LangChain, FAISS, and Google Gemini API.",
    version="1.0.0"
)

# Define and create storage directories dynamically
UPLOAD_DIR = backend_dir / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

STATIC_DIR = backend_dir.parent / "Frontend"
STATIC_DIR.mkdir(parents=True, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class AskRequest(BaseModel):
    question: str

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catches all unhandled exceptions and returns a clean, structured JSON response.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

@app.get("/")
def read_root():
    """
    Serves the static frontend index.html page.
    """
    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        # Fallback welcome JSON if index.html hasn't been created yet
        return {
            "message": "Welcome to the Document Q&A System API. Frontend index.html is missing.",
            "docs_url": "/docs",
            "health_url": "/health"
        }
    return FileResponse(html_path)

@app.get("/health")
def health_check():
    """
    Health check endpoint returning server status and environment state.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    return {
        "status": "healthy",
        "gemini_api_key_configured": api_key is not None and len(api_key) > 0
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Ingests an uploaded PDF document, parses its text, chunks the content,
    creates embedding vectors, and saves the FAISS index.
    """
    # Validate file extension
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only PDF documents are supported."
        )

    # Save file to upload directory
    file_path = UPLOAD_DIR / file.filename
    try:
        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF file is empty."
            )
        with open(file_path, "wb") as f:
            f.write(content)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to write uploaded file to disk. Error: {str(e)}"
        )

    # Extract text from the PDF
    try:
        text = extract_text_from_pdf(file_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to extract text from PDF. Error: {str(e)}"
        )

    # Split text into chunks
    try:
        chunks = split_text(text)
        if not chunks:
            raise HTTPException(
                status_code=400,
                detail="No text chunks generated from PDF content."
            )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to split text into chunks. Error: {str(e)}"
        )

    # Create embeddings and store inside FAISS
    try:
        create_vector_store(chunks)
    except ValueError as e:
        # Typically triggered if GEMINI_API_KEY is missing
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate vector store embeddings. Error: {str(e)}"
        )

    return {
        "status": "success",
        "message": f"Successfully uploaded and indexed '{file.filename}'.",
        "chunks_count": len(chunks)
    }

@app.post("/ask")
def ask_question(payload: AskRequest):
    """
    Performs similarity search on the local FAISS index, builds a contextual
    prompt, and queries Google Gemini for the answer.
    """
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Retrieve relevant document chunks
    try:
        docs = retrieve_chunks(question)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve contexts from FAISS database. Error: {str(e)}"
        )

    # Call Gemini model
    try:
        answer = ask_llm(question, docs)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response using Gemini. Error: {str(e)}"
        )

    return {
        "question": question,
        "answer": answer,
        "retrieved_chunks": [doc.page_content for doc in docs]
    }
