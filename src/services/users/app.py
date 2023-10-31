import datetime
import logging
from typing import Annotated

import fastapi.security

from src.database import Database, Education, types  # i fell like it's bad to import db models in business logic
from src.services.login.dependencies import JWTBearer
from src.services.users import dto

router = fastapi.APIRouter(dependencies=[fastapi.Depends(JWTBearer())])


@router.get(
        "/me",
        tags=["users"],
        summary="Get current user by JWT",
        response_model=dto.UsersMeDTO,
)
async def index(
        request: fastapi.Request, db: Annotated[Database, fastapi.Depends()] = None
):
    user = await db.get_user_by_email(request.state.user["email"])
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    if user.date_of_birth:
        user.date_of_birth = user.date_of_birth.strftime("%Y-%m-%d")
    projects_to_show = []
    if user.projects_to_show:
        for p in user.projects_to_show:
            if p:
                project = await db.get_project_by_id(int(p))
                if project:
                    projects_to_show.append([project.id, project.name, project.description])
            else:
                logging.warning(f"User {user.id} has empty project to show")
    user.projects_to_show = projects_to_show

    return dto.UsersMeDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronym=user.patronym,
            email=user.email,
            role=user.role,
            avatar=user.avatar,
            date_of_birth=user.date_of_birth,
            education=dto.EducationTypes(
                    primary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end], image=x.image
                        )
                        for x in user.education
                        if x.education_type == "primary"
                    ],
                    secondary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end], image=x.image
                        )
                        for x in user.education
                        if x.education_type == "secondary"
                    ],
            ),
            hobbies=user.hobbies,
            about=user.about,
            social_networks=user.social_networks,
            speciality=user.speciality,
            priority_direction=user.priority_direction,
            not_priority_direction=user.not_priority_direction,
            level=user.level,
            competencies=user.competencies,
            projects_to_show=user.projects_to_show,
            projects=user.projects,
            is_expert=user.is_expert,
            users_allow_to_show_contacts=user.users_allow_to_show_contacts,
    )


@router.patch(
        "/me",
        tags=["users"],
        summary="Update current user by JWT",
        response_model=dto.UsersMeDTO,
)
async def update(
        request: fastapi.Request,
        data: dto.UsersPatchRequestDTO,
        db: Annotated[Database, fastapi.Depends()] = None,
):
    user = await db.get_user_by_email(request.state.user["email"])
    manual_fields = ["date_of_birth", "education", "social_networks"]
    for field in data.model_dump(exclude_unset=True):
        if field in manual_fields:
            continue  # TODO: rework education with frontend
        setattr(user, field, data.model_dump()[field])
    if data.date_of_birth:
        user.date_of_birth = datetime.datetime.strptime(
                data.date_of_birth, "%Y-%m-%d"
        ).date()

    if data.education:
        if user.education:
            user.education = []
        for edu in data.education.primary_education:
            if len(edu.education_dates) != 2:
                raise fastapi.HTTPException(
                        400, {"message": "Invalid education dates"}
                )
            user.education.append(
                    Education(
                            name=edu.name,
                            education_start=edu.education_dates[0],
                            education_end=edu.education_dates[1],
                            image=edu.image,
                            education_type="primary",
                    ))
        for edu in data.education.secondary_education:
            if len(edu.education_dates) != 2:
                raise fastapi.HTTPException(
                        400, {"message": "Invalid education dates"}
                )
            user.education.append(
                    Education(
                            name=edu.name,
                            education_start=edu.education_dates[0],
                            education_end=edu.education_dates[1],
                            image=edu.image,
                            education_type="secondary",
                    ))

    if data.social_networks:
        if user.social_networks:
            social_networks = types.SocialNetworks(ok=user.social_networks.ok,
                                                   telegram=user.social_networks.telegram,
                                                   vk=user.social_networks.vk)
        else:
            social_networks = types.SocialNetworks()
        for field in data.social_networks.model_dump(exclude_unset=True):
            setattr(social_networks, field, data.social_networks.model_dump()[field])
        user.social_networks = social_networks

    res = await db.update_user(user)
    if res.date_of_birth:
        res.date_of_birth = res.date_of_birth.strftime("%Y-%m-%d")
    projects_to_show = []
    if user.projects_to_show:
        for p in user.projects_to_show:
            if p:
                project = await db.get_project_by_id(int(p))
                if project:
                    projects_to_show.append([project.id, project.name, project.description])
            else:
                logging.warning(f"User {user.id} has empty project to show")
    user.projects_to_show = projects_to_show
    return dto.UsersMeDTO(
            id=user.id,
            first_name=res.first_name,
            last_name=res.last_name,
            patronym=res.patronym,
            email=res.email,
            role=res.role,
            avatar=res.avatar,
            date_of_birth=res.date_of_birth,
            education=dto.EducationTypes(
                    primary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end]
                        )
                        for x in res.education
                        if x.education_type == "primary"
                    ],
                    secondary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end]
                        )
                        for x in res.education
                        if x.education_type == "secondary"
                    ],
            ),
            hobbies=res.hobbies,
            about=res.about,
            social_networks=res.social_networks,
            speciality=user.speciality,
            priority_direction=user.priority_direction,
            not_priority_direction=user.not_priority_direction,
            level=user.level,
            competencies=user.competencies,
            projects_to_show=user.projects_to_show,
            projects=user.projects,
            is_expert=user.is_expert,
            users_allow_to_show_contacts=user.users_allow_to_show_contacts,
    )

@router.get(
        "/experts",
        tags=["users"],
        summary="Get experts",
        response_model=list[dto.UsersMeDTO],
)
async def get_experts(
        db: Annotated[Database, fastapi.Depends()] = None,
):
    users = await db.get_experts()
    return [
        dto.UsersMeDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                patronym=user.patronym,
                email=user.email,
                role=user.role,
                avatar=user.avatar,
                date_of_birth=user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
                education=dto.EducationTypes(
                        primary_education=[
                            dto.EducationDTO(
                                    name=x.name, education_dates=[x.education_start, x.education_end]
                            )
                            for x in user.education
                            if x.education_type == "primary"
                        ],
                        secondary_education=[
                            dto.EducationDTO(
                                    name=x.name, education_dates=[x.education_start, x.education_end]
                            )
                            for x in user.education
                            if x.education_type == "secondary"
                        ],
                ),
                hobbies=user.hobbies,
                about=user.about,
                social_networks=user.social_networks,
                speciality=user.speciality,
                priority_direction=user.priority_direction,
                not_priority_direction=user.not_priority_direction,
                level=user.level,
                competencies=user.competencies,
                projects_to_show=user.projects_to_show,
                projects=user.projects,
                is_expert=user.is_expert,
                users_allow_to_show_contacts=user.users_allow_to_show_contacts,
        )
        for user in users
    ]

@router.get(
        "/{id}",
        tags=["users"],
        summary="Get user by id",
        response_model=dto.UsersMeDTO,
)
async def get_by_id(
        id: int,
        db: Annotated[Database, fastapi.Depends()] = None,
):
    user = await db.get_user(id)
    if not user:
        raise fastapi.HTTPException(400, {"message": "User not found"})
    if user.date_of_birth:
        user.date_of_birth = user.date_of_birth.strftime("%Y-%m-%d")
    projects_to_show = []
    if user.projects_to_show:
        for p in user.projects_to_show:
            if p:
                project = await db.get_project_by_id(int(p))
                if project:
                    projects_to_show.append([project.id, project.name, project.description])
    user.projects_to_show = projects_to_show
    return dto.UsersMeDTO(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            patronym=user.patronym,
            email=user.email,
            role=user.role,
            avatar=user.avatar,
            date_of_birth=user.date_of_birth,
            education=dto.EducationTypes(
                    primary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end]
                        )
                        for x in user.education
                        if x.education_type == "primary"
                    ],
                    secondary_education=[
                        dto.EducationDTO(
                                name=x.name, education_dates=[x.education_start, x.education_end]
                        )
                        for x in user.education
                        if x.education_type == "secondary"
                    ],
            ),
            hobbies=user.hobbies,
            about=user.about,
            social_networks=user.social_networks,
            speciality=user.speciality,
            priority_direction=user.priority_direction,
            not_priority_direction=user.not_priority_direction,
            level=user.level,
            competencies=user.competencies,
            projects_to_show=user.projects_to_show,
            projects=user.projects,
            is_expert=user.is_expert,
            users_allow_to_show_contacts=user.users_allow_to_show_contacts,
    )