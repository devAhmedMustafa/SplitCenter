from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Header
from .push_service import RemotePushService, get_remote_push_service

router = APIRouter(prefix="/remote/push", tags=["remote", "push"])

from .push_remote_dto import PushRemoteDto, NegotiationResponseDto


@router.get("/negotiate/{repo_id}", response_model=NegotiationResponseDto)
async def negotiate_push(
    repo_id: str,
    push_service: RemotePushService = Depends(get_remote_push_service)
):

    try:
        return await push_service.negotiate_push(repo_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/upload", response_model=dict)
async def push(
    push_dto: PushRemoteDto,
    push_service: RemotePushService = Depends(get_remote_push_service),
    files: list[UploadFile] = File(...),
    authorization: str = Header(...)
):
    try:
        await push_service.push(push_dto.repo_id, push_dto.filepathes, files)
        return {"status": "success"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))