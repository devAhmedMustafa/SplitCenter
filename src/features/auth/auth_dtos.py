from pydantic import BaseModel

class LoginRequest(BaseModel):
    token: str
    

class LoginResponse(BaseModel):
    id: str
    email: str
    token: str