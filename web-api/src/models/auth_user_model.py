from pydantic import BaseModel


class AuthUserModel(BaseModel):
    user_id: int
    token: str
