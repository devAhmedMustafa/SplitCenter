from pydantic import BaseModel

class RepoResponse(BaseModel):
    id: str
    name: str
    is_active: bool
    url: str
    owner: str