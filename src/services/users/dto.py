from typing import Optional, Annotated, List

import pydantic
from pydantic import Field

from src.database import types


def to_lower_camel(string: str) -> str:
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class CamelCaseModel(pydantic.BaseModel):
    class Config:
        alias_generator = to_lower_camel
        populate_by_name = True
        allow_population_by_alias = True
        use_enum_values = True
        # from_attributes = True


class EducationDTO(CamelCaseModel):
    name: str = Field(alias="organizationName")
    education_dates: Annotated[list[str], 2] = Field(alias="educationDates")
    image: Optional[str] = Field(None)


class EducationTypes(CamelCaseModel):
    primary_education: list[EducationDTO] = Field(alias="firstEducation")
    secondary_education: list[EducationDTO] = Field(alias="secondaryEducation")

class SocialNetworksDTO(CamelCaseModel):
    vk: Optional[str] = Field(None)
    telegram: Optional[str] = Field(None)
    ok: Optional[str] = Field(None)

class UsersMeDTO(CamelCaseModel):
    id: Optional[int]
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    patronym: Optional[str] = Field(alias="patronym")
    email: str
    role: str
    avatar: Optional[str]
    date_of_birth: Optional[str] = Field(alias="dateOfBirth")
    education: Optional[EducationTypes]
    hobbies: Optional[str]
    about: Optional[str]
    social_networks: SocialNetworksDTO = Field(alias="socialNetworks")
    speciality: Optional[str]
    priority_direction: Optional[List[str]] = Field(alias="priorityDirection")
    not_priority_direction: Optional[List[str]] = Field(alias="notPriorityDirection")
    level: Optional[str]
    competencies: Optional[str]
    projects_to_show: Optional[list] = Field(alias="projectsToShow")
    projects: Optional[list]
    is_expert: Optional[bool] = Field(alias="isExpert")
    users_allow_to_show_contacts: Optional[list] = Field(alias="usersAllowToShowContacts")

    @pydantic.validator("social_networks", pre=True)
    def validate_social_networks(cls, v):
        if not v:
            return SocialNetworksDTO()
        if isinstance(v, types.SocialNetworks):
            return SocialNetworksDTO(**v.__dict__)
        return SocialNetworksDTO(**v)

class ProjectUsersDTO(CamelCaseModel):
    id: Optional[int]
    first_name: Optional[str] = Field(alias="firstName")
    last_name: Optional[str] = Field(alias="lastName")
    patronym: Optional[str] = Field(alias="patronym")
    avatar: Optional[str]
    social_networks: Optional[SocialNetworksDTO] = Field(alias="socialNetworks")
    email: Optional[str]
    speciality: Optional[str]
    priority_direction: Optional[List[str]] = Field(alias="priorityDirection")
    not_priority_direction: Optional[List[str]] = Field(alias="notPriorityDirection")
    level: Optional[str]
    competencies: Optional[str]

    @pydantic.validator("social_networks", pre=True)
    def validate_social_networks(cls, v):
        if not v:
            return SocialNetworksDTO()
        if isinstance(v, types.SocialNetworks):
            return SocialNetworksDTO(**v.__dict__)
        return SocialNetworksDTO(**v)


class ExpertDTO(UsersMeDTO):
    id: int

class UsersMeDTOORM(pydantic.BaseModel):
    user_id: int = Field(alias="userId")
    project_id: int = Field(alias="projectId")
    class Config:
        orm_mode = True
        populate_by_name = True



class UsersPatchRequestDTO(pydantic.BaseModel):
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    patronym: Optional[str] = Field(None,alias="patronym")
    avatar: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    education: Optional[EducationTypes] = None
    hobbies: Optional[str] = None
    about: Optional[str] = None
    social_networks: Optional[SocialNetworksDTO] = Field(None, alias="socialNetworks")
    speciality: Optional[str] = None
    priority_direction: Optional[List[str]] = Field(None, alias="priorityDirection")
    not_priority_direction: Optional[List[str]] = Field(None, alias="notPriorityDirection")
    level: Optional[str] = None
    competencies: Optional[str] = None
    projects_to_show: Optional[list] = Field(None,alias="projectsToShow")
    is_expert: Optional[bool] = Field(None,alias="isExpert")
    users_allow_to_show_contacts: Optional[list] = Field(None,alias="usersAllowToShowContacts")

    @pydantic.validator("social_networks", pre=True)
    def validate_social_networks(cls, v):
        if not v:
            return SocialNetworksDTO()
        if isinstance(v, types.SocialNetworks):
            return SocialNetworksDTO(**v.__dict__)
        return SocialNetworksDTO(**v)
