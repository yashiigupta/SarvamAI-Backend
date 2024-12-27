from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key="AIzaSyDp9dg0ydqcXHSU_f7VmolKjdB5Nz8BOgw")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def aiResponse(query: str, messages: list = None, system_prompt: str = None):
    if messages is None:
        messages = []

    # Transform messages to match the expected format for Google Generative AI
    history = [
      {
        "parts": [
            {
                "text": m["message"]
            }
        ],
        "role": m["role"]
      }
      for m in messages
      if m["role"] != "system"
    ]
    
    # Include system prompt in initial chat session
    if system_prompt:
      chat_session = model.start_chat(history=[{"parts": [{"text": system_prompt}], "role": "user"}] + history)
    else:
      chat_session = model.start_chat(history=history)
    
    response = chat_session.send_message(query)
    return response

def getGreeting(topic: str):
    query = f"You have to greet the user; they want to talk about {topic}"
    response = aiResponse(query)
    return response.text