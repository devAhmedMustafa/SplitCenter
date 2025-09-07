from pydantic import BaseModel

class RepoResponse(BaseModel):
    id: str
    name: str
    url: str
    owner_id: str