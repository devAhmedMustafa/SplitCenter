from fastapi import APIRouter, UploadFile, File, Query
from fastapi.responses import StreamingResponse
from io import BytesIO
from src.utils.hash import decode_string

router = APIRouter("/storage", tags=["upload"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    filepath: str = Query(...)):

    file_location = f".data/{decode_string(filepath)}"
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"file_url": file_location}

@router.get("/download/{filepath}")
async def get_file(filepath: str):
    file_location = f".data/{filepath}"
    try:
        content = BytesIO()
        with open(file_location, "rb") as f:
            content.write(f.read())

        content.seek(0)

        return StreamingResponse(content, media_type="application/octet-stream")
    
    except FileNotFoundError:
        return {"error": "File not found"}
