# Document Q&A System

A complete Document Q&A system that lets users upload PDF files and ask questions in natural language. The project uses FastAPI for the backend, a simple frontend for uploading and querying, and local file-based storage for indexed document chunks.

## Features
- Upload PDF files through the backend
- Extract text from PDFs
- Split content into smaller text chunks
- Retrieve relevant chunks locally
- Answer questions with a local fallback response

## Project Structure
- Backend/: FastAPI backend and document processing services
- Frontend/: Simple HTML/CSS/JS interface
- README.md: Project overview and usage instructions

## Run Locally
1. Open the project folder.
2. Activate the virtual environment:
   - PowerShell: `.venv\Scripts\Activate.ps1`
3. Start the backend:
   ```powershell
   cd Backend
   ..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
   ```
4. Open the browser at `http://127.0.0.1:8000/`.

## Notes
- The current implementation uses a local fallback for retrieval and answer generation so it runs without the blocked LangChain DLL dependency.
- Upload a PDF first, then ask questions through the API or frontend.
>>>>>>> 47ae761 (Initial commit)
