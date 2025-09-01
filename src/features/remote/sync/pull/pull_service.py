from fastapi import Depends
from zipfile import ZipFile
from lib.pyscm.pyscm_api import PyscmApi
from src.features.remote.remote_service import RemoteService, get_remote_service
from io import BytesIO

class RemotePullService:

    def __init__(self, repo_service: RemoteService):
        self.repo_service = repo_service

    async def pull_repository(self, repo_id: str, commit: str):

        try:
            repo = self.repo_service.get_remote_repo(repo_id)
            if not repo:
                raise ValueError("Repository not found")

            files = PyscmApi.negotiate(repo.url, commit).split("\n")
            print(files)

            buffer = BytesIO()

            with ZipFile(buffer, "w") as zip_file:
                for file in files:
                    if not file.strip():
                        continue
                    
                    full_path = repo.url + "/" + file

                    with open(full_path, "rb") as f:
                        file_data = f.read()
                        zip_file.writestr(f"./{file}", file_data)
                

            buffer.seek(0)
            return buffer

        except Exception as e:
            print(f"Error pulling repository: {e}")
            raise ValueError(f"Error pulling repository: {e}")
        


def get_remote_pull_service(repo_service: RemoteService = Depends(get_remote_service)):
    return RemotePullService(repo_service)