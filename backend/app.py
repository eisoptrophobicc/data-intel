import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from pydantic import BaseModel
from run_query import run_query
from adapter import adapt_result

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

    return adapt_result(result, req.question)