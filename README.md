# 📚 Academic RAG Assistant

A Retrieval-Augmented Generation (RAG) application for answering questions from a collection of academic research papers.

The system retrieves relevant document chunks from a ChromaDB vector store and provides them to a Groq-hosted LLM as context. The generation layer is explicitly instructed to answer **only from the retrieved context** and to avoid guessing when the available documents do not contain enough information.

## ✨ Features

* 📄 Academic PDF document corpus
* 🔎 Semantic similarity search using Sentence Transformers
* 🗄️ Persistent ChromaDB vector store
* 🤖 Groq LLM for answer generation
* 🛡️ Context-grounded generation to reduce hallucinations
* 📎 Source filenames included with generated answers
* ⚡ FastAPI REST API
* 💬 Streamlit web interface
* 🧪 Automated backend tests
* 📊 Retrieval/evaluation artifacts
* 📓 Reproducible RAG pipeline notebook
* 🐳 Docker-ready backend
* 🔐 Environment-based API key configuration

---

# 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    └──────────┬──────────┘
                               │
                         POST /query
                               │
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Retrieval Service   │
                    └──────────┬──────────┘
                               │
                    Semantic similarity
                               │
                               ▼
              ┌────────────────────────────────┐
              │       ChromaDB Vector Store    │
              │        academic_rag collection  │
              └────────────────┬───────────────┘
                               │
                         Top-k chunks
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Generation Service  │
                    │      Groq LLM       │
                    └──────────┬──────────┘
                               │
                    Grounded answer
                    + source filenames
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Streamlit Frontend  │
                    └─────────────────────┘


Documents
   │
   ▼
PDF loading → Chunking → Embeddings → ChromaDB
```

### RAG pipeline

1. Academic PDFs are loaded and processed.
2. Documents are split into smaller chunks.
3. Each chunk is converted into an embedding using `all-MiniLM-L6-v2`.
4. Embeddings and document metadata are stored in ChromaDB.
5. A user question is converted into an embedding.
6. ChromaDB retrieves the most relevant chunks.
7. The retrieved chunks are passed to the Groq LLM as context.
8. The LLM generates an answer using the provided context.
9. Source filenames are returned with the answer.

---

# 🧰 Tech Stack

| Component            | Technology                               |
| -------------------- | ---------------------------------------- |
| Programming Language | Python                                   |
| Backend              | FastAPI                                  |
| API Server           | Uvicorn                                  |
| Frontend             | Streamlit                                |
| Vector Database      | ChromaDB                                 |
| Embeddings           | Sentence Transformers                    |
| Embedding Model      | `sentence-transformers/all-MiniLM-L6-v2` |
| LLM Provider         | Groq                                     |
| LLM Model            | `openai/gpt-oss-120b`                    |
| Configuration        | Pydantic Settings                        |
| Testing              | Pytest                                   |
| Containerization     | Docker                                   |
| Notebook             | Jupyter                                  |

---

# 📁 Project Structure

```text
academic-rag-assistant/
│
├── backend/
│   └── backend/
│       ├── app/
│       │   ├── api/
│       │   │   └── routes/
│       │   │       └── query.py
│       │   ├── core/
│       │   │   └── config.py
│       │   ├── schemas/
│       │   │   └── query.py
│       │   ├── services/
│       │   │   ├── retrieval.py
│       │   │   └── generation.py
│       │   ├── utils/
│       │   └── main.py
│       │
│       ├── tests/
│       │   └── test_query.py
│       ├── Dockerfile
│       ├── requirements.txt
│       └── .env.example
│
├── data/
│   ├── pdfs/
│   │   ├── paper_001.pdf
│   │   ├── ...
│   │   └── paper_024.pdf
│   ├── metadata.csv
│   └── verification.md
│
├── models/
│   └── vectorstore/
│       ├── chroma.sqlite3
│       ├── config.json
│       └── <Chroma index files>
│
├── frontend/
│   └── frontend/
│       ├── app.py
│       ├── api_client.py
│       └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── reports/
│   ├── corpus_inspection.csv
│   ├── evaluation_results.csv
│   └── evaluation_results_labelled.csv
│
├── .gitignore
└── README.md
```

> The nested `backend/backend` and `frontend/frontend` directories are part of the current project structure.

---

# 📚 Data and Domain

The application is designed for **academic research question answering**.

The current sample corpus contains **24 research papers** covering topics such as:

* Machine learning
* Deep learning
* Medical image analysis
* Medical image classification
* Medical image segmentation
* Clinical prediction
* Explainable AI
* Genomics
* Bioinformatics
* Multi-omics analysis
* Transfer learning
* Clinical decision support

The repository contains:

```text
data/pdfs/
```

with the sample academic documents and:

```text
data/metadata.csv
```

with document metadata.

The indexed ChromaDB collection is:

```text
academic_rag
```

and currently contains approximately **1,801 indexed document chunks**.

---

# 🔐 Why the Corpus and Vector Store Are Included

The project requirements state that large raw corpora and vector stores should generally be excluded from Git repositories.

For this implementation, the indexed sample corpus and ChromaDB store are included because:

* The sample corpus contains only 24 documents.
* The ChromaDB persistence directory is approximately 17 MB.
* The artifacts are small enough for this educational project.
* Including them allows a new user to run the application immediately after cloning.
* The repository therefore does not require the user to rebuild the vector database before testing the application.

If the corpus or vector store becomes significantly larger in a future version, they should be moved to external storage or Git LFS, and the README should be updated with download/regeneration instructions.

---

# 🚀 Getting Started

## Requirements

Install the following before starting:

* Python 3.11+
* Git
* Internet connection
* A Groq API key

Optional:

* Docker Desktop
* VS Code
* Jupyter

A GPU is **not required** to run the application.

---

# 1. Clone the Repository

```bash
git clone https://github.com/nadamohamed-10/academic-rag-assistant.git
cd academic-rag-assistant
```

---

# 2. Create a Virtual Environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is unavailable, the environment can still be used directly:

```powershell
.\.venv\Scripts\python.exe
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

# 3. Install Backend Dependencies

From the repository root:

```bash
pip install -r backend/backend/requirements.txt
```

---

# 4. Configure Environment Variables

Create a `.env` file in the **repository root**:

```text
GROQ_API_KEY=your_groq_api_key_here
```

The repository includes:

```text
backend/backend/.env.example
```

as a safe configuration template.

### Important

Never commit your actual `.env` file or Groq API key.

The `.gitignore` excludes:

```text
.env
.venv/
__pycache__/
*.log
```

---

# 5. Start the Backend

From the repository root:

```powershell
cd backend/backend
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 6. Verify the Backend

Open:

```text
http://127.0.0.1:8000/docs
```

or test the API directly:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# 7. Configure the Frontend

Create:

```text
frontend/frontend/.env
```

with:

```text
API_BASE_URL=http://127.0.0.1:8000
```

The frontend uses this environment variable instead of hard-coding the backend URL.

For deployment, this value can be changed to the public backend URL without modifying the source code.

---

# 8. Install Frontend Dependencies

Open a second terminal and activate the virtual environment.

Then:

```powershell
cd frontend/frontend
pip install -r requirements.txt
```

---

# 9. Start the Streamlit Frontend

From:

```text
frontend/frontend
```

run:

```powershell
streamlit run app.py
```

Streamlit will normally open:

```text
http://localhost:8501
```

The application should display:

> 📚 Academic RAG Assistant
> Ask a question grounded in your indexed documents.

---

# 🔌 API Reference

## GET `/health`

Checks whether the backend is running.

### Request

```bash
curl http://127.0.0.1:8000/health
```

### Response

```json
{
  "status": "ok"
}
```

---

## POST `/query`

Retrieves relevant document chunks and generates a grounded answer.

### Request

```json
{
  "question": "What is machine learning?"
}
```

### cURL

```bash
curl -X POST "http://127.0.0.1:8000/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is machine learning?\"}"
```

For macOS/Linux:

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is machine learning?"}'
```

### Example Response

```json
{
  "answer": "Machine learning is ... [paper_014.pdf].",
  "sources": [
    "paper_002.pdf",
    "paper_003.pdf",
    "paper_014.pdf",
    "paper_021.pdf"
  ]
}
```

The exact answer and retrieved sources may vary depending on the query.

---

# 🛡️ Grounding Strategy

One of the main goals of this project is to prevent the LLM from answering questions using its own general knowledge.

The generation layer uses a system instruction requiring the model to:

* Use only the supplied retrieved context.
* Cite the source documents used in the answer.
* Avoid unsupported claims.
* Say that there is not enough information when the provided context does not contain the answer.

Conceptually:

```text
User Question
      ↓
Question Embedding
      ↓
ChromaDB Similarity Search
      ↓
Top-k Retrieved Chunks
      ↓
Context-only Prompt
      ↓
Groq LLM
      ↓
Grounded Answer
      +
Source Documents
```

### Out-of-domain behaviour

The system was tested with questions that are outside the indexed academic corpus.

For example:

> What is the capital of Japan?

When the retrieved context does not contain the answer, the generation layer responds that there is not enough information instead of providing an unsupported answer.

This provides a basic grounding safeguard against relying on the LLM's general knowledge.

---

# 📊 Evaluation

Evaluation artifacts are available under:

```text
reports/
```

including:

```text
reports/corpus_inspection.csv
reports/evaluation_results.csv
reports/evaluation_results_labelled.csv
```

The evaluation set contains **13 questions**:

* 12 in-domain questions
* 1 out-of-domain question

The questions cover topics such as:

* Medical AI
* Deep learning
* Clinical prediction
* Explainable AI
* Genomics
* Multi-omics
* Transfer learning
* Clinical decision support
* AI deployment challenges

The evaluation also includes an unsupported/out-of-domain question to test whether the assistant avoids hallucinating an answer.

### Evaluation summary

| Test                                             | Result |
| ------------------------------------------------ | -----: |
| Evaluation questions                             |     13 |
| In-domain questions                              |     12 |
| Out-of-domain questions                          |      1 |
| Answers with source traceability                 |  13/13 |
| Unsupported question handled without fabrication |    1/1 |
| Context-grounded generation                      |    Yes |

Detailed results are available in:

```text
reports/evaluation_results.csv
```

and:

```text
reports/evaluation_results_labelled.csv
```

---

# 🧪 Testing

Backend tests can be executed with:

```powershell
cd backend/backend
pytest tests/
```

The test suite uses mocked services where appropriate, so the tests do not depend on making live LLM requests.

For an end-to-end test:

```bash
curl http://127.0.0.1:8000/health
```

Then:

```bash
curl -X POST "http://127.0.0.1:8000/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"How are convolutional neural networks used in medical image analysis?\"}"
```

---

# 🧠 RAG Pipeline Notebook

The main notebook is:

```text
notebooks/rag_pipeline.ipynb
```

It contains the document processing, retrieval/indexing, and evaluation workflow.

The notebook should be reproducible from a clean kernel.

### Reproducibility check

After cloning the repository:

1. Create a fresh virtual environment.
2. Install the required dependencies.
3. Open `notebooks/rag_pipeline.ipynb`.
4. Select the newly created environment as the Jupyter kernel.
5. Restart the kernel.
6. Run **Run All**.
7. Verify that the notebook executes without relying on manually created variables from previous sessions.

This is the recommended verification procedure before submission.

---

# 🖼️ Screenshots

Screenshots of the running application should be stored under:

```text
docs/screenshots/
```

Recommended screenshots:

```text
docs/
└── screenshots/
    ├── app-home.png
    ├── grounded-answer.png
    └── unsupported-question.png
```

Then add them to this section:

```markdown
## Application

![Application Home](docs/screenshots/app-home.png)

![Grounded Answer](docs/screenshots/grounded-answer.png)

![Unsupported Question](docs/screenshots/unsupported-question.png)
```

### Recommended screenshots

**1. Application Home**

Show the Streamlit interface before submitting a question.

**2. Grounded Answer**

Show a question, generated answer, and displayed source documents.

**3. Unsupported Question**

Show an out-of-domain question and the assistant's insufficient-information response.

---

# 🐳 Docker

The backend contains a Dockerfile:

```text
backend/backend/Dockerfile
```

Build the backend image from the repository root:

```bash
docker build -t academic-rag-backend ./backend/backend
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env academic-rag-backend
```

Then verify:

```bash
curl http://127.0.0.1:8000/health
```

> For production deployment, ensure the container has access to the ChromaDB vector store and that the hosting platform provides the required persistent files/storage.

---

# 🌐 Deployment

The application can be deployed as two services:

```text
                 ┌──────────────────────┐
                 │ Streamlit Frontend    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │ FastAPI Backend      │
                 └──────────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 ▼                      ▼
          ┌─────────────┐        ┌─────────────┐
          │  ChromaDB   │        │    Groq     │
          │ Vector Store│        │     LLM     │
          └─────────────┘        └─────────────┘
```

For deployment:

1. Deploy the FastAPI backend.
2. Configure `GROQ_API_KEY` as a backend secret.
3. Ensure the backend can access `models/vectorstore/`.
4. Deploy the Streamlit frontend.
5. Set `API_BASE_URL` to the deployed backend URL.
6. Configure backend CORS origins if required.
7. Test `/health`.
8. Test multiple in-domain questions.
9. Test at least one unsupported question.

---

# ⚠️ Troubleshooting

## `ModuleNotFoundError`

Make sure the correct virtual environment is active:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then reinstall dependencies:

```powershell
pip install -r backend/backend/requirements.txt
```

## Groq authentication error

Check that the root `.env` contains:

```text
GROQ_API_KEY=your_key_here
```

Do not put the API key directly inside Python source code.

## Backend cannot find the vector store

The backend expects:

```text
models/vectorstore/
```

with the:

```text
academic_rag
```

ChromaDB collection.

If the vector store is missing, regenerate it using the notebook's indexing pipeline.

## Frontend cannot connect to backend

Check:

```text
frontend/frontend/.env
```

and make sure:

```text
API_BASE_URL=http://127.0.0.1:8000
```

The FastAPI server must also be running.

## Empty retrieval results

Verify that the ChromaDB collection exists and contains indexed chunks.

The current project collection contains approximately:

```text
1,801 chunks
```

---

# 🔒 Security

Never commit:

* `.env`
* API keys
* passwords
* tokens
* private credentials
* virtual environments
* log files containing secrets

The repository's `.gitignore` excludes:

```text
.env
.venv/
__pycache__/
*.log
```

A safe `.env.example` is included for configuration guidance.

---

# ✅ Stranger Verification Checklist

Before submitting or sharing the project, verify it exactly as a new user would.

### Repository

* [ ] Clone the GitHub repository into a fresh directory.
* [ ] No API keys are committed.
* [ ] `.env` is excluded.
* [ ] `.venv/` is excluded.
* [ ] `*.log` is excluded.

### Backend

* [ ] Create a fresh virtual environment.
* [ ] Install dependencies using the README.
* [ ] Configure `GROQ_API_KEY`.
* [ ] Start FastAPI.
* [ ] `/health` works.
* [ ] `/docs` opens.
* [ ] `/query` returns grounded answers.

### Frontend

* [ ] Configure `API_BASE_URL`.
* [ ] Start Streamlit.
* [ ] Frontend connects to backend.
* [ ] Questions return answers and sources.

### RAG

* [ ] Test several different in-domain questions.
* [ ] Test an unsupported/out-of-domain question.
* [ ] Verify the assistant does not fabricate unsupported information.
* [ ] Verify source filenames are returned.

### Notebook

* [ ] Restart the kernel.
* [ ] Run all cells from the beginning.
* [ ] No manual cell-order dependency exists.

### Submission

* [ ] Evaluation results are included.
* [ ] Screenshots are included.
* [ ] API documentation is included.
* [ ] Setup instructions work on a clean machine.

---

# 📌 Repository

**GitHub:**
https://github.com/nadamohamed-10/academic-rag-assistant

---

# 👩‍💻 Project

**Academic RAG Assistant**

A student project demonstrating a complete Retrieval-Augmented Generation pipeline from academic documents to a working API and web application.
