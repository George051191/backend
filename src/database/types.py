import datetime
import enum
from typing import List, Any

import sqlalchemy
from sqlalchemy import MetaData, PrimaryKeyConstraint, ARRAY
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

my_metadata = MetaData()


class Base(DeclarativeBase):
    metadata = my_metadata


class UserRoles(str, enum.Enum):
    user = enum.auto()
    organizer = enum.auto()
    admin = enum.auto()
    expert = enum.auto()

    def __str__(self):
        return self.name


class Education(Base):
    __tablename__ = "education"
    id: Mapped[int] = mapped_column(autoincrement=True)
    name: Mapped[str]
    education_start: Mapped[str] = mapped_column(sqlalchemy.String)
    education_end: Mapped[str] = mapped_column(sqlalchemy.String)
    diploma_img: Mapped[str] = mapped_column(nullable=True)
    education_type: Mapped[str] = mapped_column(default="primary")
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    image: Mapped[str] = mapped_column(nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint(
                "id",
                "user_id",
        ),
    )

class SocialNetworks(Base):
    __tablename__ = "social_networks"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    vk: Mapped[str] = mapped_column(nullable=True)
    telegram: Mapped[str] = mapped_column(nullable=True)
    ok: Mapped[str] = mapped_column(nullable=True)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    patronym: Mapped[str] = mapped_column(nullable=True)  # or mother name
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    role: Mapped[UserRoles] = mapped_column(
            sqlalchemy.Enum(UserRoles), default=UserRoles.user
    )
    avatar: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[datetime.date] = mapped_column(sqlalchemy.Date, nullable=True)
    education: Mapped[List["Education"]] = relationship(lazy="joined", cascade="all, delete-orphan")
    hobbies: Mapped[str] = mapped_column(nullable=True)
    about: Mapped[str] = mapped_column(nullable=True)
    social_networks: Mapped["SocialNetworks"] = relationship(lazy="joined", cascade="all, delete-orphan")
    created_at: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, default=sqlalchemy.func.now()
    )
    last_login: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, nullable=True
    )
    verified_email: Mapped[bool] = mapped_column(default=False)
    speciality: Mapped[str] = mapped_column(nullable=True)
    priority_direction: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True)
    not_priority_direction: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True)
    level: Mapped[str] = mapped_column(nullable=True)
    competencies: Mapped[str] = mapped_column(nullable=True)
    projects_to_show: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.Integer), nullable=True, default=[])
    projects: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True, default=[])
    projects_requests: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True, default=[])
    projects_responses: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True, default=[])  # TODO: сделать
    # m2m с таблицей заявок, а не эту дичь
    is_expert: Mapped[bool] = mapped_column(nullable=True)
    users_allow_to_show_contacts: Mapped[List[str]] = mapped_column(ARRAY(sqlalchemy.String), nullable=True)


class Project(Base):
    # foreign key owner
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    name: Mapped[str] = mapped_column()
    idea: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    stage: Mapped[str] = mapped_column(nullable=True)
    achievements: Mapped[List[str]] = mapped_column(sqlalchemy.ARRAY(sqlalchemy.String), default=[], nullable=True)
    year: Mapped[str] = mapped_column(nullable=True)
    division: Mapped[str] = mapped_column(nullable=True)
    images: Mapped[List[str]] = mapped_column(sqlalchemy.ARRAY(sqlalchemy.String), default=[], nullable=True)
    file: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    team: Mapped[List[dict[str, str | int]]] = mapped_column(
            sqlalchemy.ARRAY(sqlalchemy.JSON), nullable=True
    )
    experts: Mapped[List[dict[str, Any]]] = mapped_column(
            sqlalchemy.ARRAY(sqlalchemy.JSON), nullable=True
    )
    description_fullness: Mapped[int] = mapped_column()
    is_published: Mapped[bool] = mapped_column(default=False)
    users_invited_in_project: Mapped[List["User"]] = relationship(secondary="user_invited",uselist=True,
                                                                            lazy='subquery')
    users_responded_to_project: Mapped[List["User"]] = relationship(secondary="user_responded", uselist=True,
                                                                    lazy='subquery')
    created_at: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, default=sqlalchemy.func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, default=sqlalchemy.func.now()
    )


class UserInvited(Base):
    __tablename__ = "user_invited"
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("projects.id"))

    __table_args__ = (
        PrimaryKeyConstraint(
                "user_id",
                "project_id",
        ),
    )


class UserResponded(Base):
    __tablename__ = "user_responded"
    user_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("projects.id"))
    user = relationship("User", backref="responded_projects")

    __table_args__ = (
        PrimaryKeyConstraint(
                "user_id",
                "project_id",
        ),
    )


class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id", ondelete='CASCADE'))
    folder_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("achievement_folder.id", ondelete='CASCADE'), index=True)
    description: Mapped[str] = mapped_column()
    files: Mapped[List[str]] = mapped_column(sqlalchemy.ARRAY(sqlalchemy.String), default=[], nullable=True)
    date: Mapped[str] = mapped_column()  # storing date as string? No problem TODO
    created_at: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, default=sqlalchemy.func.now()
    )


class AchievementFolder(Base):
    __tablename__ = "achievement_folder"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("users.id"), index=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
            sqlalchemy.DateTime, default=sqlalchemy.func.now()
    )

