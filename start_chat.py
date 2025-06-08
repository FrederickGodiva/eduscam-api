from pydantic import BaseModel


class StartChatRequest(BaseModel):
    phone_number: str
