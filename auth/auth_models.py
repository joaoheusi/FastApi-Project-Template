from pydantic import BaseModel

class AuthToken(BaseModel):
    accessToken: str
    tokenType: str

class AuthForm(BaseModel):
    username:str
    password:str