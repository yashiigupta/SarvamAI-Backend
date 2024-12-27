import json
import os
import sys

from fastapi import APIRouter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.database import execute_query
from controller.ai import aiResponse
from controller.ai import getGreeting

router = APIRouter()

defaultTopics = {
    1: "Just Vent",
    2: "Learn about something new",
    3: "Easy tips for more efficient sleep",
    4: "Help me plan my vacation",
    5: "Write the perfect email",
    6: "Relationship advice",
    7: "Brainstorm ideas",
    8: "How to get fit",
    9: "I have got my own idea"
}


@router.get("/ai/create-chat")
def create_chat(userToken: str, description: str = None, type: int = 9):
    if not description:
        description = defaultTopics[type]
    insert_query = """
    INSERT INTO chat_data (user_token, description, data) VALUES (%s, %s, %s);
    """
    data = [{"role": "system", "message": "This chat is about the topic: " + description}]
    greeting = getGreeting(description)
    data.append({"role": "assistant", "message": greeting})
    json_data = json.dumps(data)
    new_id = execute_query(insert_query, (userToken, description, json_data))
    
    select_query = "SELECT * FROM chat_data WHERE id = %s"
    row_data = execute_query(select_query, (new_id,))[0]  
    
    return {"message": "chat created", "data": row_data}


@router.get("/ai/get-all-chats")
def get_all_chats(usertoken: str):
    query = """
    SELECT * FROM chat_data WHERE user_token = %s;
    """
    chats = execute_query(query, (usertoken,))
    if not chats:
        return {"message": "no chats found"}
    return {"message": "chats found", "data": chats}

@router.get("/ai/get-chat")
def get_chat(usertoken: str, chatid: int):
    query = """
    SELECT * FROM chat_data WHERE user_token = %s AND id = %s;
    """
    chat = execute_query(query, (usertoken, chatid))
    if not chat:
        return {"message": "chat not found"}
    return {"message": "chat found", "data": chat[0]}

@router.post("/ai/send-message")
def chat(usertoken: str, chatid: int, message: str):
    query = """
    SELECT * FROM chat_data WHERE user_token = %s AND id = %s;
    """
    chat = execute_query(query, (usertoken, chatid))
    if not chat:
        return {"message": "chat not found"}
    chat = chat[0]
    data = json.loads(chat["data"])
    response = aiResponse(message, data, "Only give your answers in maximum of 150 words. This chat is about the topic: " + chat["description"])
    data.append({"role": "user", "message": message})
    data.append({"role": "assistant", "message": response.text})
    json_data = json.dumps(data)
    update_query = """
    UPDATE chat_data SET data = %s WHERE id = %s;
    """
    execute_query(update_query, (json_data, chatid))
    return {"message": "message sent", "response": response.text}