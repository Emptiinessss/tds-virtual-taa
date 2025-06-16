from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import json

# Load knowledge base
with open("tds-knowledge-base.json", "r") as f:
    knowledge_base = json.load(f)

app = FastAPI()

# Request format
class QuestionRequest(BaseModel):
    question: str
    image: str = None  # base64 encoded image (optional)

# Response format
class AnswerResponse(BaseModel):
    answer: str

@app.post("/api/", response_model=AnswerResponse)
def get_answer(data: QuestionRequest):
    question = data.question.lower()

    # 🔍 Simple keyword search in the knowledge base
    for item in knowledge_base:
        if question in item["content"].lower():
            return {"answer": item["content"]}

    # 🧠 If no exact match, fallback dummy answer
    return {"answer": "Sorry, I couldn't find an exact match. Please contact a TA for help."}
