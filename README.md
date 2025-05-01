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

## ⚙️ Setup Instructions

### 🧪 Prerequisites

- Python 3.11+
- Docker (optional)
- OpenAI API key: https://platform.openai.com/account/api-keys

---

### 🛠️ Local Setup

```bash
git clone https://github.com/your-username/LLM-Teaching-Assistant.git
cd LLM-Teaching-Assistant

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export OPENAI_API_KEY=sk-...  # your key here
uvicorn backend.main:app --reload
```

Visit: http://localhost:8000/docs

---

### 🐳 Docker

```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 -e OPENAI_API_KEY=sk-... fastapi-app
```

---

## ✅ API Endpoints

| Endpoint                          | Method | Description                                      |
|-----------------------------------|--------|--------------------------------------------------|
| `/assistants`                     | POST   | Create an assistant (inquiry or document)        |
| `/assistants/{id}/read`           | POST   | Send a prompt to the assistant                   |
| `/assistants/{id}/upload`         | PUT    | Upload more files to an existing doc assistant   |
| `/documents/save`                 | POST   | Save a document to the database                  |
| `/documents/{filename}`           | GET    | Read a document from the database                |
| `/documents`                      | GET    | List all stored documents                        |
| `/documents/import/{filename}`    | POST   | Load a file from `/documents/` into the database |

---

## 💻 Frontend Usage

1. Open `frontend/index.html` in your browser  
2. Use the input fields to:  
   - Create an assistant (inquiry or document)  
   - Send prompts  
   - Receive AI-generated responses  

---

## 🔒 GitHub Actions CI

- Automatically builds and tests the app on each push
- Requires `OPENAI_API_KEY` to be set in:
  - GitHub → Settings → Secrets → Actions → `OPENAI_API_KEY`

---

## 🧠 Built With

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI Assistants API](https://platform.openai.com/docs/assistants/overview)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
```
