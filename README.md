# 🚀 Document Q&A System

Production-ready Document Q&A app with a Streamlit frontend and a Python backend. It supports uploading a PDF, extracting text, indexing local chunks, and asking questions about the document.

## 📖 Project Overview

This project is a Document Question Answering system built with Python, Streamlit, FastAPI, PyMuPDF, and local JSON-based chunk storage.

It allows users to:

- Upload PDF documents
- Extract text using PyMuPDF
- Split text into chunks
- Store chunks locally for retrieval
- Ask questions about the uploaded document

## ✨ Features

- 📄 PDF upload and ingestion
- 📑 PDF text extraction using PyMuPDF
- ✂️ Text chunking
- 🔎 Keyword-based retrieval from local chunks
- 🤖 Local fallback answer generation
- 🚀 Streamlit web app for easy use
- 📚 Simple deployment support for Streamlit Community Cloud

## 🛠 Technology Stack

- Python 3.12
- Streamlit
- FastAPI
- PyMuPDF
- Local JSON-based chunk storage
- Optional Gemini API key support via environment variables

## 📂 Project Structure

```text
Document QA system/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── Backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── uploads/
│   ├── faiss_index/
│   └── services/
│       ├── pdf_reader.py
│       ├── text_chunker.py
│       ├── vector_store/
│       │   ├── faiss_store.py
│       │   └── retriever.py
│       └── llm/
│           └── gemini.py
└── README.md
```

## 🚀 Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Streamlit Community Cloud

This repository is prepared for deployment on Streamlit Community Cloud.

1. Push this repository to GitHub.
2. Open Streamlit Community Cloud.
3. Select the repository and main branch.
4. Set the main file to app.py.
5. Deploy.

## 🔐 Environment Variables

Create a `.env` file if you want to use Gemini-based configuration.

```env
GEMINI_API_KEY=your_google_api_key_here
```

=======
### 4. Configure environment variables
Create a .env file in the project root if you want to use the optional Gemini-related configuration.

```ini
GEMINI_API_KEY=your_api_key_here
```

> Do not push your .env file to GitHub. The repository is already configured to ignore it.

## Run Locally
From the Backend folder, run:

>>>>>>> 332ceff (Prepare Streamlit Community Cloud deployment)
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8002
```

<<<<<<< HEAD
Server:

```
http://127.0.0.1:8000
```

Swagger Docs:

```
http://127.0.0.1:8000/docs
```

---

# 📚 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Root API |
| POST | /upload | Upload PDF |
| POST | /ask | Ask Question |

---

# 📌 API Examples

## Upload PDF

```http
POST /upload
```

Response

```json
{
  "status": "success",
  "message": "PDF uploaded successfully",
  "chunks": 18
}
```

---

## Ask Question

```http
POST /ask
```

Request

```json
{
  "question": "What is machine learning?"
}
```

Response

```json
{
  "answer": "Machine learning is..."
}
```

---

# 🧠 Core Concepts

## FAISS

FAISS stores document embeddings locally and performs high-speed similarity search to retrieve the most relevant chunks.

---

## Embeddings

Embeddings convert text into high-dimensional vectors so semantically similar content can be retrieved efficiently.

---

## Google Gemini

Gemini receives the retrieved document context along with the user's question and generates a context-aware answer.

---

# ⚡ Design Decisions

- FastAPI for high-performance REST APIs
- FAISS for local vector search
- LangChain for RAG orchestration
- Gemini 2.5 Flash for answer generation
- PyMuPDF for fast PDF parsing

---

# 🐛 Troubleshooting

### ModuleNotFoundError

Activate your virtual environment and install dependencies.

```bash
pip install -r requirements.txt
```

---

### API Key Error

Ensure `.env` contains a valid Google API key.

```env
GOOGLE_API_KEY=your_google_api_key
```

---

### FAISS Error

Upload at least one PDF before using the `/ask` endpoint.

---

# 🔒 Files Not to Push

```
.env
uploads/
faiss_index/
__pycache__/
.venv/
```

---

# 🚀 Future Improvements

- Multi-document support
- Authentication
- Conversation history
- Cloud Vector Database
- Streaming responses
- Docker support

---

# 👨‍💻 Author

**Priyanshu Vishwakarma**

GitHub: https://github.com/priyanshu9937
=======
### Local URLs
- Swagger docs: http://127.0.0.1:8002/docs
- Redoc docs: http://127.0.0.1:8002/redoc
- Health check: http://127.0.0.1:8002/health

## API Endpoints
- GET / - API root information
- GET /health - Health check
- POST /upload - Upload a PDF file and index it locally
- POST /ask - Ask a question about the uploaded document

## Example Requests

### Upload a PDF
```bash
curl -X POST "http://127.0.0.1:8002/upload" \
  -H "accept: application/json" \
  -F "file=@/path/to/file.pdf"
```

### Ask a question
```bash
curl -X POST "http://127.0.0.1:8002/ask" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What is this document about?\"}"
```

## Notes
- The project is currently backend-only.
- Uploaded PDFs and generated chunk indexes are stored locally and are ignored by Git.
- The app does not require a frontend folder to run.

## License
MIT
>>>>>>> 332ceff (Prepare Streamlit Community Cloud deployment)
