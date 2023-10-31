import datetime
from typing import Optional, Any

import pydantic
from pydantic import Field

from src.services.users.dto import UsersMeDTOORM, UsersMeDTO, ProjectUsersDTO


class Project(pydantic.BaseModel):
    owner_id: Optional[int] = Field(None, alias="ownerId")
    name: str = Field(None)
    idea: Optional[str] = Field(None)
    status: Optional[str] = Field(None)
    stage: Optional[str] = Field(None)
    achievements: list[str] = Field(default=[])
    year: Optional[str] = Field(None)
    division: Optional[str] = Field(None)
    images: list[str] = Field(default=[])
    file: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    team: list[dict[str, str | int]] = Field(default=[])
    experts: list[dict[str, Any]] = Field(default=[])
    description_fullness: int = Field(alias="descriptionFullness", default=0)
    is_published: bool = Field(alias="isPublished", default=False)
    users_invited_in_project: list[ProjectUsersDTO] = Field(None, alias="usersInvitedInProject")
    users_responded_to_project: list[ProjectUsersDTO] = Field(None,alias="usersRespondedToProject")
    created_at: Optional[datetime.datetime] = Field(None, alias="createdAt")

class ProjectResponseDTO(Project):
    id: int

    @pydantic.validator("users_invited_in_project", pre=True)
    def validate_users_invited(cls, v):
        return [ProjectUsersDTO(**user.__dict__) for user in v]

    @pydantic.validator("users_responded_to_project", pre=True)
    def validate_users_responded(cls, v):
        return [ProjectUsersDTO(**user.__dict__) for user in v]
    class Config:
        orm_mode = True
        populate_by_name = True


class ProjectUpdateRequestDTO(Project):
    project_id: int = Field(alias="projectId")
    class Config:
        orm_mode = True


class ProjectCreateRequestDTO(Project):
    class Config:
        orm_mode = True


# dto.ProjectPublishRequestDTO
class ProjectPublishRequestDTO(pydantic.BaseModel):
    publish: bool
    project_id: int = Field(alias="projectId")




class ProjectRespondRequestDTO(pydantic.BaseModel):
    project_id: int = Field(alias="projectId")


class ProjectInviteRequestDTO(pydantic.BaseModel):
    project_id: int = Field(alias="projectId")
    user_id: int = Field(alias="userId")


class ProjectApproveRequestDTO(pydantic.BaseModel):
    project_id: int = Field(alias="projectId")
    user_id: int = Field(alias="userId")
    user_speciality: str = Field(alias="userSpeciality")
    user_name: str = Field(alias="userName")

class ProjectDenyRequestDTO(pydantic.BaseModel):
    project_id: int = Field(alias="projectId")
    user_id: int = Field(alias="userId")

class ProjectShareContactDTO(pydantic.BaseModel):
    shown: bool
    project_id: int = Field(alias="projectId")