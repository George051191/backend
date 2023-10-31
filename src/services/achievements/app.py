import random
import string
from typing import Annotated, List, Optional

import fastapi
from fastapi import UploadFile, File

from src.database import Database, AchievementFolder, Achievement
from src.services.achievements import dto
from src.services.login.dependencies import JWTBearer
import src.settings

router = fastapi.APIRouter(dependencies=[fastapi.Depends(JWTBearer())])


@router.get("/", tags=["achievements"], summary="Get all achievement folders",
        response_model=list[dto.AchievementFoldersDTO], )
async def get_all(request: fastapi.Request, db: Annotated[Database, fastapi.Depends()],
):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    res = await db.get_folders_by_user(user.id)
    return [dto.AchievementFoldersDTO(**r.__dict__) for r in res]

@router.post("/", tags=["achievements"], summary="Create achievement folder",
             response_model=dto.AchievementFoldersDTO)
async def create(
        request: fastapi.Request,
        data: dto.AchievementFoldersDTO,
        db: Annotated[Database, fastapi.Depends()],
):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    folder = AchievementFolder(
        owner_id=user.id,
        name=data.name,
    )
    res = await db.create_folder(folder)
    return dto.AchievementFoldersDTO(**res.__dict__)

@router.get("/{id}", tags=["achievements"], summary="Get achievement folder by id",
        response_model=List[dto.AchievementDTO] )
async def get_by_id(
        id: int,
        db: Annotated[Database, fastapi.Depends()],
):
    res = await db.get_achievements_by_folder(id)
    return [dto.AchievementDTO(**r.__dict__) for r in res]

@router.patch("/{folder_id}", tags=["achievements"], summary="Update achievement folder by id",
        response_model=dto.AchievementFoldersDTO)
async def update(
        folder_id: int,
        data: dto.AchievementFoldersDTO,
        db: Annotated[Database, fastapi.Depends()],
):
    folder = await db.get_folder_by_id(folder_id)
    if not folder:
        raise fastapi.HTTPException(400, {"message": "Folder not found"})
    folder.name = data.name
    res = await db.update_folder(folder)
    return dto.AchievementFoldersDTO(**res.__dict__)

@router.delete("/{folder}", tags=["achievements"], summary="Delete achievement folder by id")
async def delete(
        folder: int,
        db: Annotated[Database, fastapi.Depends()],
):
    folder = await db.get_folder_by_id(folder)
    if not folder:
        raise fastapi.HTTPException(400, {"message": "Folder not found"})
    await db.delete_folder(folder.id)
    return {"success": True}

@router.get("/{folder_id}/{achievement_id}", tags=["achievements"], summary="Get achievement by id",
            response_model=dto.AchievementDTO)
async def get_by_id(
        folder_id: int,
        achievement_id: int,
        db: Annotated[Database, fastapi.Depends()],
):
    res = await db.get_achievement_by_id(achievement_id)
    return dto.AchievementDTO(**res.__dict__)

@router.delete("/{folder_id}/{achievement_id}", tags=["achievements"], summary="Delete achievement by id")
async def delete(
        folder_id: int,
        achievement_id: int,
        db: Annotated[Database, fastapi.Depends()],
):
    achievement = await db.get_achievement_by_id(achievement_id)
    if not achievement:
        raise fastapi.HTTPException(400, {"message": "Achievement not found"})
    await db.delete_achievement(achievement.id)
    return {"success": True}

@router.post("/{folder}", tags=["achievements"], summary="Create achievement",
                response_model=dto.AchievementDTO)
async def create(
        folder: int,
        db: Annotated[Database, fastapi.Depends()],
        data: dto.AchievementDTO,
):
    # settings = src.settings.Settings() # remake that
    folder = await db.get_folder_by_id(folder)
    # files = []
    # for file in uploaded_files:
    #     file.filename = ("".join(random.choices(string.ascii_uppercase + string.digits, k=10))  + "." +
    #                      file.filename.split(
    #             ".")[-1])
    #     open(settings.FILES_PATH + file.filename, "wb").write(file.file.read())
    #     files.append(file.filename)
    if not folder:
        raise fastapi.HTTPException(400, {"message": "Folder not found"})
    achievement = Achievement(
        owner_id=folder.owner_id,
        folder_id=folder.id,
        name=data.name,
        description=data.description,
        files=data.files,
        date=data.date,
    )
    res = await db.create_achievement(achievement)

    return dto.AchievementDTO(id=res.id,createdAt=res.created_at , name=res.name, description=res.description, files=res.files, date=res.date)

@router.patch("/{folder_id}/{achievement_id}", tags=["achievements"], summary="Update achievement by id",
                response_model=dto.AchievementDTO)
async def update(
        folder_id: int,
        achievement_id: int,
        data: dto.AchievementDTO,
        db: Annotated[Database, fastapi.Depends()],
):
    # settings = src.settings.Settings()
    folder = await db.get_folder_by_id(folder_id)
    # files = []
    # for file in uploaded_files:
    #     file.filename = ("".join(random.choices(string.ascii_uppercase + string.digits, k=10)) + "." +
    #                      file.filename.split(
    #             ".")[-1])
    #     open(settings.FILES_PATH + file.filename, "wb").write(file.file.read())
    #     files.append(file.filename)
    if not folder:
        raise fastapi.HTTPException(400, {"message": "Folder not found"})
    achievement = await db.get_achievement_by_id(achievement_id)
    if not achievement:
        raise fastapi.HTTPException(400, {"message": "Achievement not found"})
    achievement.name = data.name
    achievement.description = data.description
    achievement.files = data.files #TODO: make actual files, not base64
    achievement.date = data.date
    res = await db.update_achievement(achievement)
    return dto.AchievementDTO(**res.__dict__)

