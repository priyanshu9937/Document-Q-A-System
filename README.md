<div align="center">
  <h1>🚀 Document Q&A System (RAG Pipeline)</h1>
  <p>Production-ready Document Q&A System built with Python 3.12, FastAPI, Google Gemini, LangChain, FAISS, and PyMuPDF.</p>

  <!-- Badges -->
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Gemini-2.5_Flash-4285F4?logo=google&logoColor=white" alt="Google Gemini"></a>
  <a href="https://python.langchain.com/"><img src="https://img.shields.io/badge/LangChain-Integration-1C3C3C?logo=langchain&logoColor=white" alt="LangChain"></a>
  <a href="https://github.com/facebookresearch/faiss"><img src="https://img.shields.io/badge/FAISS-Vector_Store-blue" alt="FAISS"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</div>

---

## 📖 Project Overview
This project is a high-performance, production-ready **Document Q&A System** that allows users to upload PDF documents and ask natural language questions about their contents. It leverages a robust **Retrieval-Augmented Generation (RAG)** pipeline to ensure accurate, context-bounded answers without hallucinations.

## ✨ Features
- **PDF Ingestion:** Upload and process PDF documents quickly using `PyMuPDF`.
- **Advanced Text Chunking:** Semantically splits text using LangChain's `RecursiveCharacterTextSplitter`.
- **Vector Storage:** Fast, local similarity search using Facebook AI Similarity Search (`FAISS`).
- **Google Gemini Integration:** Harnesses the power of `Gemini 2.5 Flash` for highly accurate generation.
- **RESTful API:** Built with FastAPI, providing auto-generated Swagger documentation.
- **Modern UI:** Glassmorphic, responsive web interface for easy interaction.

## 🛠 Technology Stack
- **Backend Framework:** FastAPI (Python 3.12)
- **LLM:** Google Gemini 2.5 Flash
- **Embeddings:** Google Embedding API (`models/embedding-001`)
- **Orchestration:** LangChain
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **PDF Extraction:** PyMuPDF
- **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Glassmorphism)

## 🏗 Architecture

```text
+----------------+      +----------------+      +------------------+
|   User Client  | ---> |   FastAPI App  | ---> |   PDF Extractor  |
|   (Frontend)   |      |   (/upload)    |      |    (PyMuPDF)     |
+----------------+      +----------------+      +------------------+
                                                         |
                                                         v
                                                +------------------+
                                                |   Text Chunker   |
                                                |   (LangChain)    |
                                                +------------------+
                                                         |
+----------------+      +----------------+               v
| Google Gemini  | <--- |   FAISS Store  | <--- +------------------+
| (models/flash) |      | (Vector Index) |      | Embeddings Model |
+----------------+      +----------------+      +------------------+
        |                        ^
        |                        |
        v                        |
+----------------+      +----------------+
|   User Client  | <--- |   FastAPI App  |
|   (Response)   |      |     (/ask)     |
+----------------+      +----------------+
```

## 🔄 RAG Workflow
1. **Upload PDF**: User uploads a document.
2. **Extract text**: PyMuPDF extracts raw text from the file.
3. **Split into chunks**: Text is broken down into manageable semantic chunks.
4. **Generate embeddings**: Google Embedding API converts text into vectors.
5. **Store in FAISS**: Vectors are saved locally for fast retrieval.
6. **Retrieve relevant chunks**: When a question is asked, FAISS finds the most relevant chunks.
7. **Send context + question to Gemini**: LangChain orchestrates sending the prompt to Gemini.
8. **Return answer**: The user receives a context-aware answer.

## 📂 Folder Structure
```text
Document QA system/
├── Frontend/                      # Frontend static assets
│   ├── index.html                 # HTML structure
│   ├── style.css                  # Custom CSS variables, glassmorphic layout
│   └── app.js                     # JavaScript client handling uploads & queries
├── Backend/                       # Backend FastAPI application
│   ├── uploads/                   # Stored uploaded PDF documents (Git ignored)
│   ├── faiss_index/               # Local FAISS index database (Git ignored)
│   ├── services/                  # Core RAG pipeline services
│   │   ├── pdf_reader.py          # PyMuPDF text extractor service
│   │   ├── text_chunker.py        # LangChain text splitting service
│   │   ├── vector_store/          # Vector database sub-package
│   │   │   ├── faiss_store.py     # Embeds chunks and saves FAISS database locally
│   │   │   └── retriever.py       # Retrieves top K chunks from FAISS
│   │   └── llm/                   # Language model wrapper sub-package
│   │       └── gemini.py          # ChatGoogleGenerativeAI connector
│   ├── main.py                    # Entrypoint FastAPI application
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Template for environment configuration
├── .gitignore                     # Ignored files configuration
└── README.md                      # Project documentation
```

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Rudra05x/document-qa-system-fastapi-gemini.git
cd document-qa-system-fastapi-gemini
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate
```

### 3. Install Requirements
```bash
cd Backend
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the dummy `.env.example` file to create a real `.env` file.
```bash
cp .env.example .env
```
Inside `.env`, add your Google API key:
```ini
GOOGLE_API_KEY=your_actual_api_key_here
```
> **⚠️ Security Note:** Never push the `.env` file to GitHub!

### 5. Running the Project
```bash
uvicorn main:app --reload
```
The API will run at `http://127.0.0.1:8000/`. You can open the `Frontend/index.html` file in your browser to use the UI.

## 📚 API Documentation (Swagger)
FastAPI automatically generates interactive API documentation.
- **Swagger URL:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### API Endpoints
- `GET /` - Health check and API root
- `POST /upload` - Upload a PDF document and index its contents
- `POST /ask` - Ask a natural language question about the uploaded document

### Example Requests & Responses

**Upload API (`/upload`)**
```bash
curl -X POST "http://127.0.0.1:8000/upload" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@/path/to/document.pdf"
```
```json
{
  "status": "success",
  "message": "Successfully uploaded and indexed 'document.pdf'.",
  "chunks_count": 14
}
```

**Ask API (`/ask`)**
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"question\": \"What is the summary of section 2?\"}"
```
```json
{
  "question": "What is the summary of section 2?",
  "answer": "According to the document, section 2 details the deployment guidelines.",
  "retrieved_chunks": [
    "Section 2: Database Schema & Deployment Guidelines..."
  ]
}
```

## 🧠 Core Concepts

### How FAISS works
FAISS (Facebook AI Similarity Search) is an open-source library that enables efficient similarity search of dense vectors. When a user asks a question, FAISS computes vector distances (e.g., L2 Euclidean distance) between the query vector and the document vectors to return the most semantically relevant chunks in microseconds.

### How Embeddings work
An embedding is a vector representation of text in a high-dimensional space. Words or documents with similar semantic meanings are located close to one another in this vector space, making it possible to mathematically search for text meaning rather than exact keyword matches.

### How Gemini is used
Google Gemini 2.5 Flash acts as the generator in our pipeline. Once FAISS retrieves the relevant text chunks, they are injected into Gemini's prompt alongside the original question. Gemini reads this context and synthesizes a clear, factual answer.

## 📸 Screenshots
*(Add placeholders for screenshots here)*
- <img width="1859" height="898" alt="image" src="https://github.com/user-attachments/assets/bd52b2ce-0fa5-4fb3-8150-9315750f3a41" />

-<img width="1893" height="897" alt="image" src="https://github.com/user-attachments/assets/9b8ffd7c-9e56-4c72-ba4d-57a492f4141b" />


- <img width="1890" height="902" alt="image" src="https://github.com/user-attachments/assets/b3724d5a-d815-4957-bdec-367b757376f9" />


## ⚡ Performance Notes & Design Decisions
- **Why FastAPI:** Chosen for its extremely high performance, async support, and native Swagger documentation out of the box.
- **Why FAISS:** Selected over cloud vector databases (like Pinecone) to eliminate network latency, remove cloud costs, and keep all document data strictly local and secure.
- **Why LangChain:** Used as the orchestration layer to easily integrate PyMuPDF text splitting, Google Embeddings, and the LLM via standardized wrappers.

## 🎓 How to Explain this Project in an Interview
**Q: Describe the architecture of your Document QA system.**
*A: It's a localized Retrieval-Augmented Generation (RAG) system. A user uploads a PDF, which PyMuPDF extracts text from. LangChain splits this text into chunks, and the Google Embedding API converts them into high-dimensional vectors stored in a local FAISS index. When a user asks a question, we embed the query, perform a similarity search in FAISS to get the top context chunks, and feed those into Google Gemini via a carefully structured prompt to generate a final, factual response.*

**Q: Why use Retrieval-Augmented Generation (RAG)?**
*A: LLMs like Gemini have a knowledge cutoff and can hallucinate facts. RAG solves this by providing the LLM with a strictly bounded context retrieved from a trusted source (the uploaded PDF), forcing the model to cite and synthesize only the provided information.*

## 🐛 Troubleshooting & Debugging
- **ModuleNotFoundError:** Ensure your virtual environment is active and `pip install -r requirements.txt` has been run.
- **API Key Error:** Double-check that your `.env` file is named exactly `.env` and `GOOGLE_API_KEY` is valid.
- **FAISS Load Error:** Make sure you have uploaded a document first. The FAISS index is generated dynamically upon upload.

## 🔒 Version Control Guidelines
**What SHOULD NOT be pushed to GitHub:**
- `.env` (Contains sensitive API keys)
- `Backend/uploads/` (Contains user PDFs)
- `Backend/faiss_index/` (Contains generated vector databases)
- `__pycache__/`, `.pytest_cache/`, `venv/`, `.venv/` (Local Python environments)
- `.idea/`, `.vscode/` (IDE settings)
- Any large binaries or secrets.

**What SHOULD be pushed:**
- Source code (`.py`, `.js`, `.html`, `.css`)
- `README.md`, `requirements.txt`, `.env.example`, `.gitignore`, `LICENSE`, `CONTRIBUTING.md`
- Documentation and templates.

## 🔮 Future Improvements
- Multi-document upload support.
- User authentication and conversational memory (chat history).
- Switch to a cloud-based vector DB (e.g., Pinecone/Weaviate) for horizontal scaling.

## 🤝 Contributing
Contributions are always welcome! Please see the `CONTRIBUTING.md` for guidelines.

## 📜 License
This project is licensed under the [MIT License](LICENSE).

## 👤 Author
**Rudra05x** - [GitHub Profile](https://github.com/Rudra05x)

## 🙏 Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [LangChain](https://python.langchain.com/)
- [Google Gemini](https://ai.google.dev/)
- [FAISS](https://faiss.ai/)
