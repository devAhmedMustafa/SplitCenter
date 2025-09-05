from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class SignupRequest(BaseModel):
    username: str
    password: str

class SignupResponse(BaseModel):
    id: str
    username: str

class LoginResponse(BaseModel):
    id: str
    username: str
    token: str