from pydantic import BaseModel


class MessageInputModel(BaseModel):
    sender_name: str
    text: str
