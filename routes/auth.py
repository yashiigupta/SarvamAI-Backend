import os
import sys
from uuid import uuid4

from fastapi import APIRouter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import execute_query

router = APIRouter()


@router.post("/auth/register")
async def register(username: str):
    query = """
    INSERT INTO user (username, token) VALUES (%s, %s);
    """
    token = uuid4().hex
    execute_query(query, (username, token))
    return {"message": "user registered", "token": token}



@router.get("/auth/get-user")
async def login(usertoken: str):
    query = """
    SELECT * FROM user WHERE token = %s;
    """
    
    user = execute_query(query, (usertoken,))
    if not user:
        return {"message": "user not found"}
    return {"message": "user found", "data": user[0]}