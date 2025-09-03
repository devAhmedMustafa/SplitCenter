from fastapi import APIRouter, Depends, HTTPException, Header, Form
from .push_service import RemotePushService, get_remote_push_service
import json

router = APIRouter(prefix="/remote/push", tags=["remote", "push"])

from .push_remote_dto import NegotiationResponseDto


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
    repo_id: str = Form(...),
    filepathes: str = Form(...),
    push_service: RemotePushService = Depends(get_remote_push_service),
    authorization: str = Header(...)
):
    try:
        presignedurls = await push_service.push(repo_id, json.loads(filepathes))
        return {"status": "success", "presigned_urls": presignedurls}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))