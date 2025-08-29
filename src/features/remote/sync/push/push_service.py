from fastapi import Depends
from lib.pyscm.pyscm_api import PyscmApi
from src.features.remote.remote_service import RemoteService, get_remote_service

from .push_remote_dto import NegotiationResponseDto

class RemotePushService:

    def __init__(
            self,
            remote_service: RemoteService
        ):
        
        self.remote_service = remote_service

    async def negotiate_push(self, repo_id: str) -> NegotiationResponseDto:

        try:
            repo = self.remote_service.get_remote_repo(repo_id)
            commits : list[str] = PyscmApi.get_commit_history(repo.url)

            print(commits)

            if commits is None:
                raise ValueError("Error fetching commit history")
            
            if len(commits) < 1:
                return NegotiationResponseDto(commit_id="EMPTY")

            return NegotiationResponseDto(commit_id=commits[-1])
        
        except Exception as e:
            raise ValueError(f"Failed to negotiate: {str(e)}")
        
def get_remote_push_service(remote_service: RemoteService = Depends(get_remote_service)) -> RemotePushService:
    return RemotePushService(remote_service)