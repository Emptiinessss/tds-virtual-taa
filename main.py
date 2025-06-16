from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
import json

app = FastAPI()

# Enable CORS (optional but helpful)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the knowledge base
with open("tds-knowledge-base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Health check route
@app.get("/")
def read_root():
    return {"message": "Hello from TDS Virtual TA!"}

# Request model
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 encoded image string

# Dummy similarity matching (replace with real one later)
def find_relevant_entries(question):
    matches = []
    for item in knowledge_base:
        if any(word.lower() in item.get("content", "").lower() for word in question.split()):
            matches.append(item)
        if len(matches) >= 2:
            break
    return matches

# POST route to handle questions
@app.post("/api/")
def answer_question(req: QuestionRequest):
    relevant = find_relevant_entries(req.question)

    links = []
    for item in relevant:
        links.append({
            "url": item.get("url", "https://example.com"),
            "text": item.get("content", "")[:100]
        })

    return {
        "answer": f"This is a placeholder answer for: '{req.question}'",
        "links": links
    }
