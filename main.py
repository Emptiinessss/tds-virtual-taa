from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
import base64
import json
import uvicorn
import os

# Load knowledge base
with open("tds-knowledge-base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None  # base64 image if provided

@app.post("/api/")
async def answer_question(request: QuestionRequest):
    user_question = request.question.lower()

    # Simple keyword search
    relevant = []
    for item in knowledge_base:
        content = (item.get("summary") or "") + " " + (item.get("content_snippet") or "")
        if user_question in content.lower():
            relevant.append({
                "url": item.get("url", ""),
                "text": item.get("summary", item.get("content_snippet", "")[:200])
            })
            if len(relevant) >= 2:
                break

    answer = (
        "Here's what I found that may help with your question. "
        "Please review the links and summaries below."
    ) if relevant else "Sorry, I couldn’t find a direct answer. Please try rephrasing or check Discourse for updates."

    return {
        "answer": answer,
        "links": relevant
    }

# For local testing
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
