from pydantic import BaseModel

class NegotiationResponseDto(BaseModel):
    commit_id: str

class PushRemoteDto(BaseModel):
    repo_id: str
    filepathes: list[str]