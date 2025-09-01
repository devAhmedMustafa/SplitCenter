from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse

from src.features.remote.sync.pull.pull_service import RemotePullService, get_remote_pull_service

router = APIRouter(prefix="/remote/pull", tags=["remote", "pull"])

@router.get("/fetch/{repoId}")
async def pull_repository(repoId: str, commit: str = Query(...), service: RemotePullService = Depends(get_remote_pull_service)):

    try:
        compressed_file = await service.pull_repository(repoId, commit)
        return StreamingResponse(
            compressed_file,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={repoId}.zip"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))