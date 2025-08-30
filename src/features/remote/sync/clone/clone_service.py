from fastapi import Depends
from zipfile import ZipFile
from lib.pyscm.pyscm_api import PyscmApi
from src.features.remote.remote_service import RemoteService, get_remote_service
from io import BytesIO

class RemoteCloneService:

    def __init__(self, repo_service: RemoteService):
        self.repo_service = repo_service

    async def clone_repository(self, repo_url: str):

        try:
            repo = self.repo_service.get_remote_repo_byurl(repo_url)
            filepaths = PyscmApi.negotiate(repo_url, "EMPTY").split("\n")

            buffer = BytesIO()

            with ZipFile(buffer, "w") as zipf:
                for filepath in filepaths:
                    if not filepath.strip():
                        continue
                    
                    full_path = repo.url + "/" + filepath
                    with open(full_path, "rb") as f:
                        file_data = f.read()
                        zipf.writestr(filepath, file_data)

            buffer.seek(0)
            return buffer, repo.id

        except Exception as e:
            raise ValueError(f"Error cloning repository: {e}")
        

def get_clone_service(repo_service: RemoteService = Depends(get_remote_service)) -> RemoteCloneService:
    return RemoteCloneService(repo_service)