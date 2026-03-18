import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from pydantic import BaseModel
from run_query import run_query
from adapter import adapt_result
from passlib.hash import bcrypt
import auth

app = FastAPI()
auth.create_users_table()

class QueryRequest(BaseModel):
    question: str
    mode: str = "new"

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

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

@app.post("/register")
def register(req: RegisterRequest):

    hashed_password = bcrypt.hash(req.password)
    auth.register_user(req.email, hashed_password, req.name)
    return {"status": "user created"}

@app.post("/login")
def login(req: LoginRequest):

    user = auth.login_user(req.email)

    if not user:
        return {"status": "error", "message": "user not found"}

    stored_hash = user[2]

    if not bcrypt.verify(req.password, stored_hash):
        return {"status": "error", "message": "invalid password"}

    return {
        "status": "success",
        "message": "login successful",
        "email": user[1]
    }