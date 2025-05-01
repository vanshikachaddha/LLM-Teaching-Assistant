```
# AutoTeacher AI 🧠📄

AutoTeacher AI is a document and inquiry assistant built with FastAPI, OpenAI's Assistant API, and a simple frontend. It supports analyzing documents, sending custom prompts, and interacting with multiple uploaded files — all through a REST API or a web interface.

---

## 🚀 Features

- 📂 Upload and analyze multiple PDF files via OpenAI's Assistant API
- 💬 Prompt-based interaction with uploaded documents (`DocBot`)
- 🧠 Inquiry-based assistant (`ChatBot`) for general Q&A
- 🗃️ Local SQLite document storage with save/read/list endpoints
- 🌐 Simple frontend (`index.html` + `app.js`) to interact with backend
- 🐳 Dockerized + GitHub Actions CI integration

---

## 📁 File Structure

```
.
├── backend/
│   ├── main.py                 # FastAPI backend
│   ├── database.py             # SQLite helpers
│   └── chatbots/
│       ├── __init__.py
│       ├── inquiry_handler.py  # ChatBot logic (OpenAI Q&A)
│       └── document_uploader.py# DocBot logic (document analysis)
│
├── db/
│   └── documents.db            # SQLite database
│
├── documents/
│   └── test2.pdf               # Example document files
│
├── frontend/
│   ├── index.html              # Simple UI
│   └── app.js                  # JS logic for interacting with backend
│
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI workflow
│
├── Dockerfile
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 🧪 Prerequisites

- Python 3.11+
- Docker (optional)
- OpenAI API key: [Get yours here](https://platform.openai.com/account/api-keys)

---

### 🛠️ Local Setup

1. Clone the repo:

```bash
git clone https://github.com/your-username/LLM-Teaching-Assistant.git
cd LLM-Teaching-Assistant
```

2. Create virtual environment + install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Export your OpenAI key:

```bash
export OPENAI_API_KEY=sk-...
```

4. Run the app:

```bash
uvicorn backend.main:app --reload
```

Then open: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🐳 Docker

```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 -e OPENAI_API_KEY=sk-... fastapi-app
```

---

### ✅ API Endpoints

#### `/assistants`  
- **POST** – Create new assistant  
- `{"type": "document", "filename": ["test2.pdf", "test3.pdf"]}`

#### `/assistants/{assistant_id}/read`  
- **POST** – Send a prompt to assistant  
- `{"prompt": "What is this PDF about?"}`

#### `/assistants/{assistant_id}/upload`  
- **PUT** – Add more documents to a document assistant

#### `/documents/save`  
- **POST** – Save content to the local database

#### `/documents/{filename}`  
- **GET** – Retrieve document from database

#### `/documents`  
- **GET** – List all saved documents

#### `/documents/import/{filename}`  
- **POST** – Import a local file from the `documents/` folder

---

### 💻 Frontend Usage

1. Open `frontend/index.html` in your browser
2. Interact with the assistant:
   - Create assistant (document/inquiry)
   - Send prompts
   - View responses

---

## 🔒 GitHub Actions CI

- Runs on every push to `main`
- Builds Docker container
- Starts server
- Hits `/docs` endpoint to verify success

Secrets needed:
- `OPENAI_API_KEY` in GitHub → Settings → Secrets → Actions

---

## 🧠 Powered By

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)

---
```
