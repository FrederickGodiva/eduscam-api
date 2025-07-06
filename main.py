import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

from agents.scammer import ScammerAgent
from agents.evaluator import EvaluatorAgent
from agents.educator import EducatorAgent
from utils.session_manager import SessionManager
from models.schemas import Message, StartChatRequest
from config.settings import settings

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()
scammer = ScammerAgent()
evaluator = EvaluatorAgent()
educator = EducatorAgent()

@app.get('/api')
def hello_world():
    return {
        "message": "Hello World"
    }

@app.post('/api/start_chat')
async def start_chat(request: StartChatRequest):
    session_id = str(uuid.uuid4())
    session = session_manager.create_session(session_id, request.phone_number)
    
    initial_message = await scammer.generate_message(session['scam_type'])
    
    # Send to WhatsApp
    chat_id = f"{request.phone_number}@c.us"
    payload = {
        "session": "default",
        "chatId": chat_id,
        "text": initial_message
    }
    
    try:
        response = requests.post(
            "http://waha:3000/api/sendText",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    session_manager.update_session(session_id, "", initial_message)
    
    return {
        "session_id": session_id,
        "message": initial_message
    }

@app.post('/api/chat')
async def chat(message: Message):
    session = session_manager.get_session(message.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Evaluate user response
    user_flag = await evaluator.evaluate_response(
        message.content,
        session['conversation_history']
    )

    # Check if simulation should end
    if user_flag == "deceived" or session['turn_counter'] >= settings.MAX_TURNS:
        feedback = await educator.generate_feedback(
            user_flag,
            session['scam_type'],
            session['conversation_history']
        )
        session['is_simulation_revealed'] = True
        return {"message": feedback, "simulation_ended": True}

    # Generate next scammer message
    response = await scammer.generate_message(
        session['scam_type'],
        message.content
    )
    
    session_manager.update_session(
        message.session_id,
        message.content,
        response,
        user_flag
    )

    return {"message": response, "simulation_ended": False}

@app.post('/api/webhook')
async def webhook(request: Request):
    try:
        # Parse incoming webhook data
        data = await request.json()
        print(data)

        payload = data.get('payload', {})
        sender_id = payload.get('from')
        text = payload.get('body')
        chat_id = payload.get('to')

        message = data.get("message")
        chat_id = data.get("chatId")
        
        if not message or not chat_id:
            raise HTTPException(status_code=400, detail="Invalid webhook data")
        
        # Process the incoming message
        session_id = chat_id  # Use chat_id as session_id for simplicity
        session = session_manager.get_session(session_id)
        
        if not session:
            # If no session exists, create a new one
            session = session_manager.create_session(session_id, chat_id)
            initial_message = await scammer.generate_message(session['scam_type'])
            session_manager.update_session(session_id, "", initial_message)
            
            # Send initial scam message back to WAHA
            return {
                "chatId": chat_id,
                "text": initial_message
            }
        
        # Evaluate user response
        user_flag = await evaluator.evaluate_response(
            message,
            session['conversation_history']
        )
        
        # Check if simulation should end
        if user_flag == "deceived" or session['turn_counter'] >= settings.MAX_TURNS:
            feedback = await educator.generate_feedback(
                user_flag,
                session['scam_type'],
                session['conversation_history']
            )
            session['is_simulation_revealed'] = True
            return {
                "chatId": chat_id,
                "text": feedback
            }
        
        # Generate next scammer message
        response = await scammer.generate_message(
            session['scam_type'],
            message
        )
        session_manager.update_session(
            session_id,
            message,
            response,
            user_flag
        )
        
        return {
            "chatId": chat_id,
            "text": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
