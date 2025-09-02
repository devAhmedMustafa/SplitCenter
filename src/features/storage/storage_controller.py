from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter("/upload", tags=["upload"])


@router.post("/")
async def upload_files(
    files: list[UploadFile] = File(...), 
    filepaths : list[str] = Form,):

    uploaded_file_paths = []
    for filepath, file in zip(filepaths, files):

        file_location = f".data/{filepath}"
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded_file_paths.append(file_location)
        
    return {"file_paths": uploaded_file_paths}

@router.get("/{filepath}")
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
