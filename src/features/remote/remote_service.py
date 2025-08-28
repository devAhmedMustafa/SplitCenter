from fastapi import Depends
from .link_remote_dtos import LinkRemoteDto
from .remote_repo import RemoteRepository, get_remote_repository
from .repository import Repository
from src.features.auth.jwt import decode_jwt_token

from lib.pyscm.pyscm_api import PyscmApi

from uuid import UUID

class RemoteService:
    def __init__(self, remote_repo: RemoteRepository = Depends(get_remote_repository)):
        self.remote_repo = remote_repo

    def link_remote_repo(self, link_remote_dto: LinkRemoteDto):

        try:

            user = decode_jwt_token(link_remote_dto.token)
            if not user or "id" not in user or "email" not in user:
                raise ValueError("Invalid token")
            
            user_id = user.get("id")
            username = user.get("email")

            url = f"./data/repos/{username}/{link_remote_dto.repo_name}"
            PyscmApi.init(url)
            
            new_repo = Repository(
                name=link_remote_dto.repo_name,
                owner=UUID(user_id),
                url=url
            )

            return self.remote_repo.create_repository(new_repo)
        
        except Exception as e:
            raise ValueError(f"Failed to link repository: {str(e)}")
        
    
    def get_remote_repo(self, repo_id: str):
        try:
            return self.remote_repo.get_repository(repo_id)
        
        except ValueError:
            raise ValueError("Repository not found")



def get_remote_service(remote_repo: RemoteRepository = Depends(get_remote_repository)) -> RemoteService:
    return RemoteService(remote_repo)

    