from pydantic import BaseModel

class LinkRemoteDto(BaseModel):
    repo_name: str
    token: str