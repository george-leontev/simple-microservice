from pydantic import BaseModel


class MailModel(BaseModel):
    uid: str
    sender: str
    reciever: str
    message: str
