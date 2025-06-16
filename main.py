from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import base64
import json

app = FastAPI()

# Enable CORS (important for cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/")
def read_root():
    return {"message": "Hello from TDS Virtual TA!"}

# Load the knowledge base
with open("tds-knowledge-base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# Define the input model
class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 encoded image

# Find relevant knowledge base entries (basic match)
def find_relevant_entries(question):
    matches = []
    for item in knowledge_base:
        content = item.get("markdown", "") + item.get("content", "")
        if any(word.lower() in content.lower() for word in question.split()):
            matches.append(item)
        if len(matches) >= 2:
            break
    return matches

# POST endpoint to handle question
@app.post("/api/")
def answer_question(req: QuestionRequest):
    relevant = find_relevant_entries(req.question)

    links = []
    for item in relevant:
        links.append({
            "url": item.get("url", "https://example.com"),
            "text": item.get("content", item.get("markdown", ""))[:100]
        })

    return {
        "answer": f"This is a placeholder answer for: '{req.question}'",
        "links": links
    }
