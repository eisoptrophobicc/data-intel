import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from pydantic import BaseModel
from run_query import run_query

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    mode: str = "new"


@app.get("/")
def home():
    return {"message": "YouTube Analytics API running"}

@app.post("/query")
def query(req: QueryRequest):

    result = run_query(req.question, req.mode)

    # If error occurs just return it
    if result["status"] != "success":
        return result

    response = {
        "status": result.get("status"),
        "question": req.question,
        "intent": result.get("intent"),
        "sql": result.get("sql"),
        "data": result.get("data"),
        "chart": result.get("chart"),
        "insight": result.get("insight")
    }

    return response