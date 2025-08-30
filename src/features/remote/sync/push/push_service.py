from fastapi import Depends, UploadFile
from lib.pyscm.pyscm_api import PyscmApi
from src.features.remote.remote_service import RemoteService, get_remote_service

from .push_remote_dto import NegotiationResponseDto, PushRemoteDto

import os

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
        

    async def push(self, repo_id: str, filepathes: list[str], files: list[UploadFile]):
        try:
            repo = self.remote_service.get_remote_repo(repo_id)

            if len(filepathes) != len(files):
                raise ValueError("Filepaths and files count mismatch")
            
            for filepath, file in zip(filepathes, files):
                file_location = os.path.join(repo.url, filepath)
                os.makedirs(os.path.dirname(file_location), exist_ok=True)
                with open(file_location, "wb") as f:
                    content = await file.read()
                    f.write(content)

        except Exception as e:
            raise ValueError(f"Failed to push: {str(e)}")
        
def get_remote_push_service(remote_service: RemoteService = Depends(get_remote_service)) -> RemotePushService:
    return RemotePushService(remote_service)