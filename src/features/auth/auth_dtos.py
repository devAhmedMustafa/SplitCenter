from pydantic import BaseModel

class TokenData(BaseModel):
    token: str
    

class LoginResponse(BaseModel):
    id: str
    email: str
    token: str