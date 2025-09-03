from fastapi import Depends
from lib.pyscm.pyscm_api import PyscmApi
from src.features.remote.remote_service import RemoteService, get_remote_service
from .push_remote_dto import NegotiationResponseDto
from src.utils.aws_s3 import S3Client
from config.serttings import settings
from src.utils.hash import encode_string

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
        

    async def push(self, repo_id: str, filepathes: list[str]):
        try:

            presigned_urls: list[str] = []

            if settings.ENV == "production":
                s3_client = S3Client()
                for filepath in filepathes:
                    presigned_url = s3_client.generate_presigned_url("repos", f"{repo_id}/{filepath}", operation_name="put_object")
                    presigned_urls.append(presigned_url)

            else:
                for filepath in filepathes:
                    hashed_path = encode_string(f"repos/{repo_id}/{filepath}")
                    presigned_url = f"http://localhost:8000/storage/upload?path={hashed_path}"
                    presigned_urls.append(presigned_url)

            return presigned_urls

        except Exception as e:
            raise ValueError(f"Failed to push: {str(e)}")
        
def get_remote_push_service(remote_service: RemoteService = Depends(get_remote_service)) -> RemotePushService:
    return RemotePushService(remote_service)