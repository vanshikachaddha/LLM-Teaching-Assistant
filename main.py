from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from inquiry_handler import ChatBot
from document_uploader import DocBot
import uuid

class CreateAssistantRequest(BaseModel):
    type: str
    filename: Optional[str] = None

class AnalyzeRequest(BaseModel):
    prompt: str

app = FastAPI()
assistant_list = {}

# Create Assistant
@app.post("/assistants")
def create_assistant(request: CreateAssistantRequest):
    if (request.type == "inquiry"):
        chatbot = ChatBot()
    elif (request.type == "document"):
        if not request.filename:
            raise HTTPException(status_code=400, detail="Filename required for document assistant")
        chatbot = DocBot(request.filename)
    else:
        raise HTTPException(status_code=400, detail="Invalid assistant type")
    
    assistant_id = str(uuid.uuid4())
    assistant_list[assistant_id] = {
        "type": request.type,
        "object": chatbot
    }

    return {"assistant_id": assistant_id}

    
# Read Prompt
@app.post("/assistants/{assistant_id}/read")
def input_prompt(assistant_id: str, request: AnalyzeRequest):
    assistant_entry = assistant_list.get(assistant_id)
    if not assistant_entry:
        raise HTTPException(status_code=404, detail="Assistant not found")

    assistant_obj = assistant_entry["object"]
    assistant_type = assistant_entry["type"]

    if (assistant_type == "inquiry"):
        return {"response": assistant_obj.chat_helper(request.prompt)}
    if (assistant_type == "document"):
        return {"response": assistant_obj.doc_analyzer(request.prompt)}
    else:
        raise HTTPException(status_code=400, detail="Invalid prompt")
    
# Update Assistant
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

