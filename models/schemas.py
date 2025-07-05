from pydantic import BaseModel

class Message(BaseModel):
    session_id: str
    content: str
    phone_number: str

class StartChatRequest(BaseModel):
    phone_number: str
