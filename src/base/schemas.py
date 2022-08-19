from pydantic.main import BaseModel
from datetime import date, datetime

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class Token_auth(Token):
    exp: int
    user_id: int


class TokenPayload(BaseModel):
    user_id: int = None


class RefreshTokenUser(BaseModel):
    user_id: int
    refresh_token: str
    fingerprint: str
    ip: str
    issued: datetime
    expires_in: datetime


class Msg(BaseModel):
    msg: str



