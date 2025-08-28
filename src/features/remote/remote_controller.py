from fastapi import APIRouter, Depends, HTTPException
from .link_remote_dtos import LinkRemoteDto
from .remote_service import RemoteService, get_remote_service

router = APIRouter(prefix="/remote", tags=["remote"])

@router.post('/link')
async def create_remote(req: LinkRemoteDto,service: RemoteService = Depends(get_remote_service)):
    try:
        repo = service.link_remote_repo(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return repo

@router.get('/{repo_id}')
async def get_remote(repo_id: str, service: RemoteService = Depends(get_remote_service)):
    try:
        repo = service.get_remote_repo(repo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return repo
    