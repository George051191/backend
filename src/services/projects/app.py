from typing import Annotated

import fastapi.security

from src.database import (Database, Project, )  # i fell like it's bad to import db models in business logic
from src.services.login.dependencies import JWTBearer
from src.services.projects import dto

router = fastapi.APIRouter(dependencies=[fastapi.Depends(JWTBearer())])  #


@router.post("/create", tags=["projects"], summary="Create new project", response_model=dto.ProjectResponseDTO, )
async def create(request: fastapi.Request, data: dto.ProjectCreateRequestDTO,
        db: Annotated[Database, fastapi.Depends()] = None, ):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    if not data.team:
        data.team = []
        if user.first_name and user.last_name:
            data.team.append({"id": user.id, "name": user.first_name + " " + user.last_name,
                "speciality":       user.speciality or "Основатель", })
    project = Project(owner_id=user.id, name=data.name, idea=data.idea, status=data.status, stage=data.stage,
            achievements=data.achievements, year=data.year, division=data.division, images=data.images, file=data.file,
            description=data.description, team=data.team, experts=data.experts,
            description_fullness=data.description_fullness, is_published=data.is_published, users_invited_in_project=[],
            users_responded_to_project=[], )
    res = await db.create_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)


@router.patch("/update", tags=["projects"], summary="Update project", response_model=dto.ProjectResponseDTO, )
async def update(data: dto.ProjectUpdateRequestDTO, db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    manual_fields = ["owner_id", "created_at", "updated_at"]
    for field in data.model_dump(exclude_unset=True):
        if field in manual_fields:
            continue
        setattr(project, field, data.model_dump()[field])
    res = await db.update_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)


@router.get("/all", tags=["projects"], summary="Get all projects", response_model=list[dto.ProjectResponseDTO], )
async def get_all(db: Annotated[Database, fastapi.Depends()] = None, ):
    res = await db.get_all_projects()
    return [dto.ProjectResponseDTO(**r.__dict__) for r in res if r.is_published]


@router.get("/my", tags=["projects"], summary="Get current user projects",
        response_model=list[dto.ProjectResponseDTO], )
async def get_my(request: fastapi.Request, db: Annotated[Database, fastapi.Depends()] = None, ):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    res = await db.get_user_projects(user.id)
    return [dto.ProjectResponseDTO(**r.__dict__) for r in res]


@router.patch("/publish", tags=["projects"], summary="Publish project", response_model=dto.ProjectResponseDTO, )
async def publish(data: dto.ProjectPublishRequestDTO, db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    project.is_published = data.publish
    res = await db.update_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)


@router.patch("/respond", tags=["projects"], summary="Respond to project", response_model=dto.ProjectResponseDTO, )
async def respond(request: fastapi.Request, data: dto.ProjectRespondRequestDTO,
        db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    user = await db.get_user_by_email(request.state.user["email"])
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    if user.id in project.users_responded_to_project:
        raise fastapi.HTTPException(400, {"message": "User already responded"})
    if not project.users_responded_to_project:
        project.users_responded_to_project = []
    project.users_responded_to_project.append(user)
    res = await db.update_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)


@router.patch("/invite", tags=["projects"], summary="Invite to project", response_model=dto.ProjectResponseDTO, )
async def invite(data: dto.ProjectInviteRequestDTO, db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    if not project.users_invited_in_project:
        project.users_invited_in_project = []
    if any([data.user_id == u.id for u in project.users_invited_in_project]):
        raise fastapi.HTTPException(400, {"message": "User already invited"})
    user = await db.get_user(data.user_id)
    project.users_invited_in_project.append(user)
    res = await db.update_project(project)

    return dto.ProjectResponseDTO(**res.__dict__)

@router.patch("/approveExpert", tags=["projects"], summary="Approve expert", response_model=dto.ProjectResponseDTO, )
async def approve(data: dto.ProjectApproveRequestDTO, db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    if data.user_id in [e["id"] for e in project.team]:
        raise fastapi.HTTPException(400, {"message": "User already approved"})
    user = await db.get_user(data.user_id)
    # project.users_responded_to_project = list(filter(lambda u: u.id != user.id, project.users_responded_to_project))
    project.team.append({"id": data.user_id, "speciality": data.user_speciality, "name": data.user_name, })
    res = await db.update_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)

@router.post("/denyExpert", tags=["projects"], summary="Deny expert", response_model=dto.ProjectResponseDTO, )
async def deny(data: dto.ProjectDenyRequestDTO, db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    user = await db.get_user(data.user_id)
    project.users_responded_to_project = list(filter(lambda u: u.id != user.id, project.users_responded_to_project))
    res = await db.update_project(project)
    return dto.ProjectResponseDTO(**res.__dict__)


@router.post("/request",  # TODO: rename to avoid missunderstanding with /respond or /invite
        tags=["projects"], summary="Request to join project", response_model=dto.ProjectResponseDTO, )
async def request_join(request: fastapi.Request, data: dto.ProjectRespondRequestDTO,
        db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    user = await db.get_user_by_email(request.state.user["email"])
    if not user.projects_requests:
        user.projects_requests = []
    user.projects_requests.append(data.project_id)
    res = await db.update_user(user)
    return {"message": "ok"}


@router.post("/shareContacts", tags=["projects"], summary="Share contacts")
async def share_contacts(request: fastapi.Request, data: dto.ProjectShareContactDTO,
        db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    user = await db.get_user_by_email(request.state.user["email"])
    project.users_invited_in_project = list(filter(lambda u: u.id != user.id, project.users_invited_in_project))
    await db.update_project(project)
    # we should email him here or something
    return {"message": "ok"}

@router.post("/denyContacts", tags=["projects"], summary="Deny contacts")
async def deny_contacts(request: fastapi.Request, data: dto.ProjectShareContactDTO,
                        db: Annotated[Database, fastapi.Depends()] = None, ):
    project = await db.get_project_by_id(data.project_id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    user = await db.get_user_by_email(request.state.user["email"])
    project.users_invited_in_project = list(filter(lambda u: u.id != user.id, project.users_invited_in_project))
    await db.update_project(project)
    return {"message": "ok"}


@router.get("/requestsExperts", tags=["projects"], summary="Get experts requests to join project")
async def get_requests_experts(request: fastapi.Request, db: Annotated[Database, fastapi.Depends()] = None, ):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    user_projects = await db.get_user_projects(user.id)
    if not user_projects:
        return {"experts": []}
    projects = []
    for project in user_projects:
        if len(project.users_responded_to_project) > 0:
            projects.append(project)
    return {"projects": [dto.ProjectResponseDTO(**r.__dict__) for r in projects]}

@router.get("/requestsProjects", tags=["projects"], summary="Get projects requests to user to join project")
async def get_requests_projects(request: fastapi.Request, db: Annotated[Database, fastapi.Depends()] = None, ):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    res = await db.get_all_projects()  # TODO: write actual query lol not this shit
    # delayed because no money
    return [dto.ProjectResponseDTO(**r.__dict__) for r in res if
        any([user.id == u.id for u in r.users_invited_in_project])]


@router.get("/requestsMy", tags=["projects"], summary="Get users requests")
async def get_my_requests(request: fastapi.Request, db: Annotated[Database, fastapi.Depends()] = None,):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    projects = db.select_where_responded(user.id)
    expert_requests = []
    projects = await db.get_user_projects(user.id)
    for p in projects:
        for e in p.users_invited_in_project:
            expert_requests.append(dto.ProjectUsersDTO(**e.__dict__))
    return {"experts": expert_requests, "projects": projects}



@router.get("/{id}", tags=["projects"], summary="Get project by id", response_model=dto.ProjectResponseDTO, )
async def get_by_id(id: int, db: Annotated[Database, fastapi.Depends()] = None, ):
    res = await db.get_project_by_id(id)
    if not res:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    return dto.ProjectResponseDTO(**res.__dict__)


@router.delete("/{id}", tags=["projects"], summary="Delete the project")
async def delete_project(id: int, db: Annotated[Database, fastapi.Depends()] = None):
    project = await db.get_project_by_id(id)
    if not project:
        raise fastapi.HTTPException(400, {"message": "Project not found"})
    res = await db.delete_project(id)
    if not res:
        raise fastapi.HTTPException(400, {"message": "Project was not deleted"})
    return {"message": "ok"}
