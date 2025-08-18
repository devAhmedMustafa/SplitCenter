from pydantic import BaseModel

class TokenData(BaseModel):
    token: str
    

class LoginResponse(BaseModel):
    email: str
    token: str