from fastapi import APIRouter, Body, Depends, HTTPException, Form
from fastapi.responses import StreamingResponse
from .clone_service import RemoteCloneService, get_clone_service

router = APIRouter(prefix="/remote/clone", tags=["remote", "clone"])

@router.post("/fetch")
async def clone_repository(repo_url: str = Form(...), service: RemoteCloneService = Depends(get_clone_service)):
    try:
        compressed_file, repoId = await service.clone_repository(repo_url)

        return StreamingResponse(
            compressed_file,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={repoId}.zip"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))