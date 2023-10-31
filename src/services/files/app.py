import os

import fastapi

import src.settings

router = fastapi.APIRouter()

# read files by its name
@router.get("/{id}", tags=["files"], summary="Get file by id")
async def get_by_id(
        id: str,
):
    settings = src.settings.Settings()
    files = os.listdir(settings.FILES_PATH)
    if id not in files:
        raise fastapi.HTTPException(400, {"message": "File not found"})
    file = open(f"{settings.FILES_PATH}/{id}", "rb")
    return fastapi.responses.StreamingResponse(file, media_type="application/octet-stream")
