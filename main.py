from fastapi import FastAPI
from pydantic import BaseModel
from inquiry_handler import chat

class AnalyzeRequest(BaseModel):
    prompt: str

app = FastAPI()

@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    response = chat(request.prompt)
    return response
