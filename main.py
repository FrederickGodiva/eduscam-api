from fastapi.responses import JSONResponse
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from generate_message import generate_scam_message
from generate_response import generate_scam_response
from user_input import Message
from start_chat import StartChatRequest
import uuid
import logging

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conversations = {}

@app.get('/root')
async def root():
    return {"message:": "Hello World"}

@app.post('/start_chat')
async def start_chat(request: StartChatRequest):
    """Memulai percakapan dan mengembalikan initial message serta session_id."""
    session_id = str(uuid.uuid4())
    initial_scam_message = await generate_scam_message()

    conversations[session_id] = [{"role": "assistant", "content": initial_scam_message}]
    chat_id = f"{request.phone_number}@c.us"
    payload = {
        "session": "default",
        "chatId": chat_id,
        "text": initial_scam_message
    }
    

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post("http://waha:3000/api/sendText", json=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to send WhatsApp message: {e}")

    return {
        "session_id": session_id,
        "scammer": initial_scam_message
    }

@app.post('/chat')
async def chat(user_message: Message):
    session_id = user_message.session_id

    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session ID not found")

    response = await generate_scam_response(user_message.content, conversations[session_id]) 
    conversations[session_id].append({"role": "user", "content": user_message.content})
    conversations[session_id].append({"role": "assistant", "content": response})
    
    return {"scammer": response}


@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)

        # Extract data from WAHA-like payload
        payload = data.get('payload', {})
        sender_id = payload.get('from')
        text = payload.get('body')
        chat_id = payload.get('to')
        print(sender_id, text)

        if not sender_id or not text:
            raise ValueError("Missing 'from' or 'body' in payload")

        phone_number = sender_id.split("@")[0]

        # Session management
        session_id = None
        for sid, conv in conversations.items():
            if conv and conv[0].get('phone_number') == phone_number:
                session_id = sid
                break

        if not session_id:
            session_id = str(uuid.uuid4())
            conversations[session_id] = [{"role": "system", "phone_number": phone_number}]

        conversations[session_id].append({"role": "user", "content": text})
        print(conversations[session_id])

        # Generate response from your scam simulator or chatbot
        response = await generate_scam_response(text, conversations[session_id])
        print(response)
        conversations[session_id].append({"role": "assistant", "content": response})

        # Send message via WAHA
        payload_to_send = {
            "session": "default",
            "chatId": sender_id,  # Send back to the original sender
            "text": response
        }
        headers = {"Content-Type": "application/json"}
        res = requests.post("http://waha:3000/api/sendText", json=payload_to_send, headers=headers)
        res.raise_for_status()

        return JSONResponse(content={"status": "ok"}, status_code=200)

    except Exception as e:
        logging.error(f"Error in /webhook: {e}", exc_info=True)
        return JSONResponse(content={"error": str(e)}, status_code=500)
