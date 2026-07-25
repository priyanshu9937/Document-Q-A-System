# 🚀 Document Q&A System 

Production-ready **Document Q&A Backend** built with **Python 3.12, FastAPI, Google Gemini, LangChain, FAISS, and PyMuPDF**.

---

## 📖 Project Overview

This project is a backend implementation of a **Retrieval-Augmented Generation (RAG)** based Document Question Answering System.

It allows users to:

- Upload PDF documents
- Extract text using PyMuPDF
- Split text into semantic chunks
- Generate embeddings using Google Embedding API
- Store embeddings in a local FAISS vector database
- Retrieve relevant document chunks
- Generate context-aware answers using Google Gemini 2.5 Flash

---


Server:

```
http://127.0.0.1:8002
```

## ✨ Features

- 📄 PDF Upload API
- 📑 PDF Text Extraction using PyMuPDF
- ✂️ Semantic Text Chunking
- 🧠 Google Embedding API
- ⚡ FAISS Vector Database
- 🤖 Google Gemini 2.5 Flash Integration
- 🚀 FastAPI REST APIs
- 📚 Auto-generated Swagger Documentation

---

# 🛠 Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Programming Language |
| FastAPI | Backend Framework |
| Google Gemini 2.5 Flash | Large Language Model |
| Google Embedding API | Embeddings |
| LangChain | RAG Orchestration |
| FAISS | Vector Database |
| PyMuPDF | PDF Text Extraction |

---

# 🏗 Architecture

```text
                  +----------------+
                  |     Client     |
                  +--------+-------+
                           |
                           v
                 +-------------------+
                 | FastAPI (/upload) |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 |    PyMuPDF        |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 | Text Chunking     |
                 | (LangChain)       |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 | Google Embeddings |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 |      FAISS        |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 |    Retriever      |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 | Gemini 2.5 Flash  |
                 +--------+----------+
                          |
                          v
                 +-------------------+
                 |    Response API   |
                 +-------------------+
```

---

# 🔄 RAG Workflow

1. Upload PDF
2. Extract text from PDF
3. Split text into chunks
4. Generate embeddings
5. Store embeddings in FAISS
6. Retrieve relevant chunks
7. Send retrieved context + user question to Gemini
8. Return the generated answer

---

# 📂 Folder Structure

```text
Backend/
│
├── uploads/
│
├── faiss_index/
│
├── services/
│   ├── pdf_reader.py
│   ├── text_chunker.py
│   │
│   ├── vector_store/
│   │   ├── faiss_store.py
│   │   └── retriever.py
│   │
│   └── llm/
│       └── gemini.py
│
├── main.py
├── requirements.txt
└── .env.example
```

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone <repository-url>

cd Backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Environment File

Create a file named `.env`

```env
GOOGLE_API_KEY=your_google_api_key
```

---

## 5. Run Server

```bash
uvicorn main:app --reload
```

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
