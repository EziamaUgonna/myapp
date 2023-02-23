from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from random import sample
from typing import List
from pymongo import MongoClient
from collections import deque

app = FastAPI()
audit_log = deque(maxlen=10)
client = MongoClient("mongodb://mongo:27017")
db = client["api_logs"]
users_db = db["users"]

class JumbledWord(BaseModel):
    jumbled_word: str

class APICall(BaseModel):
    api_name: str
    payload: str

async def authenticate_user(username: str, password: str):
    user = users_db.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    if user["password"] != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return True

async def get_current_user(username: str = None, password: str = None):
    if not (username and password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    return await authenticate_user(username, password)

@app.post("/login")
async def login(username: str, password: str):
    await authenticate_user(username, password)
    return {"message": "Login successful."}

@app.get("/jumble/{word}", response_model=JumbledWord)
async def jumble(word: str):
    """
    Jumble the characters of a given word.
    """
    jumbled_word = "".join(sample(word, len(word)))
    return {"jumbled_word": jumbled_word}

@app.post("/audit", response_model=APICall)
async def log_api_call(api_call: APICall, user: bool = Depends(get_current_user)):
    """
    Logs all API calls to the server.
    """
    result = db.audit_log.insert_one(api_call.dict())
    api_call.payload = "****"
    return api_call

@app.get("/audit", response_model=List[APICall])
async def get_audit_log(user: bool = Depends(get_current_user)):
    """
    Returns the last 10 API calls made to the server.
    """
    result = db.audit_log.find().sort([('_id', -1)]).limit(10)
    return [APICall(**doc) for doc in result]

