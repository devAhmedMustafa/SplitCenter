from fastapi import APIRouter, Depends, HTTPException
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
