from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.chatbots.inquiry_handler import ChatBot
from backend.chatbots.document_uploader import DocBot
from backend.database import init_db, save_document, read_document, list_documents
import uuid
import os
import datetime
from typing import List


# Initialize database
init_db()

app = FastAPI()
assistant_list = {}

from fastapi.middleware.cors import CORSMiddleware

# Add CORS middleware to allow frontend to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins to access the API (can be restricted to specific domains)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ======== Models ========

@app.get("/")
def root():
    return {"message": "Welcome to AutoTeacher AI! Visit /docs for API documentation."}

class CreateAssistantRequest(BaseModel):
    type: str
    filename: Optional[List[str]] = None

class AnalyzeRequest(BaseModel):
    prompt: str

class SaveRequest(BaseModel):
    filename: str
    content: str

class GradeRequest(BaseModel):
    rubric_filename: str

# ======== Assistant Routes ========

@app.post("/assistants")
def create_assistant(request: CreateAssistantRequest):
    if request.type == "inquiry":
        chatbot = ChatBot()
    elif request.type == "document":
        if not request.filename or not isinstance(request.filename, list):
            raise HTTPException(status_code=400, detail="List of filenames required for document assistant")
        chatbot = DocBot(request.filename)  # Pass list of files
    else:
        raise HTTPException(status_code=400, detail="Invalid assistant type")

    assistant_id = str(uuid.uuid4())
    assistant_list[assistant_id] = {
        "type": request.type,
        "object": chatbot
    }

    return {"assistant_id": assistant_id}

@app.post("/assistants/{assistant_id}/read")
def input_prompt(assistant_id: str, request: AnalyzeRequest):
    assistant_entry = assistant_list.get(assistant_id)
    if not assistant_entry:
        raise HTTPException(status_code=404, detail="Assistant not found")

    assistant_obj = assistant_entry["object"]
    assistant_type = assistant_entry["type"]

    if assistant_type == "inquiry":
        response = assistant_obj.chat_helper(request.prompt)
    elif assistant_type == "document":
        response = assistant_obj.doc_analyzer(request.prompt)
    else:
        raise HTTPException(status_code=400, detail="Invalid assistant type")

    filename = f"{assistant_type}_{datetime.datetime.now().isoformat()}.txt"
    save_document(filename, response)

    return {"response": response, "saved_as": filename}

@app.put("/assistants/{assistant_id}/upload")
def update_file(assistant_id: str, filename: str):
    assistant_entry = assistant_list.get(assistant_id)
    if not assistant_entry:
        raise HTTPException(status_code=404, detail="Assistant not found")

    assistant_type = assistant_entry["type"]
    assistant_obj = assistant_entry["object"]

    if assistant_type != "document":
        raise HTTPException(status_code=400, detail="Only document assistants can upload new files")

    assistant_obj.add_doc(filename)
    return {"message": "File uploaded successfully"}

# ======== Document Management ========

@app.post("/documents/save")
def save_to_database(request: SaveRequest):
    save_document(request.filename, request.content)
    return {"message": f"Document '{request.filename}' saved successfully."}

@app.get("/documents/{filename}")
def get_document(filename: str):
    content = read_document(filename)
    if not content:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"filename": filename, "content": content}

@app.get("/documents")
def list_all_documents():
    return {"documents": list_documents()}

@app.post("/documents/import/{filename}")
def import_local_file(filename: str):
    path = os.path.join("documents", filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found in documents/ folder")

    try:
        with open(path, "rb") as f:
            content = f.read().decode("utf-8", errors="ignore")  # decode binary to string
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    save_document(filename, content)
    return {"message": f"'{filename}' imported from local folder."}

class CreateAssistantRequest(BaseModel):
    type: str
    filenames: Optional[list[str]] = []  # List of filenames

@app.post("/assistants")
def create_assistant(request: CreateAssistantRequest):
    if request.type == "inquiry":
        chatbot = ChatBot()
    elif request.type == "document":
        if not request.filenames:
            raise HTTPException(status_code=400, detail="At least one filename is required for document assistants")
        chatbot = DocBot(request.filenames)  # Pass the list of filenames to the DocBot
    else:
        raise HTTPException(status_code=400, detail="Invalid assistant type")

    assistant_id = str(uuid.uuid4())
    assistant_list[assistant_id] = {
        "type": request.type,
        "object": chatbot
    }

    return {"assistant_id": assistant_id}