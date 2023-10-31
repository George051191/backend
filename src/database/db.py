import fastapi
import passlib.hash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.orm import joinedload

from src.database import User, Project, Achievement, AchievementFolder, UserInvited


class Database:
    def __init__(self, ss: fastapi.Request = None):
        self.ss: async_sessionmaker = ss  # type: ignore

    async def get_session(self) -> AsyncSession:
        async with self.ss() as session:
            try:
                yield session
            except Exception as e:
                print(e)
            finally:
                await session.close()

    async def get_user(self, user_id: int) -> User | None:
        async with self.ss() as session:
            user = await session.scalar(select(User).where(User.id == user_id))
            return user

    async def get_user_by_email(self, email: str) -> User | None:
        async with self.ss() as session:
            user = await session.scalar(select(User).where(User.email == email))
            return user

    async def user_login(self, email: str, password: str) -> User | None:
        async with self.ss() as session:
            user = await session.scalar(select(User).where(User.email == email)) or User(
                    password="$argon2id$v=19$m=65536,t=3,p=4$jXFu7V2rNYaQslYKQShlLA$De8bAyhSFVr+2S/TaBBlrHeoEKwB/dhlEiMHbm5IIBM"
                    # password: 123
            )  # create fake user to prevent timing attacks
            result = passlib.hash.argon2.verify(password, user.password)
            if result and user.email == email:
                return user
            else:
                return None

    async def create_user(self, email: str, password: str, ) -> User:
        async with self.ss() as session:
            user = User(email=email, password=passlib.hash.argon2.hash(password), )
            session.add(user)
            await session.commit()
            return user

    async def update_user(self, user: User) -> User:
        async with self.ss() as session:
            await session.merge(user)
            await session.commit()
            return user

    async def set_user_password(self, user: User, new_password: str) -> User:
        async with self.ss() as session:
            user.password = passlib.hash.argon2.hash(new_password)
            await session.commit()
            return user

    async def update_project(self, project: Project) -> Project:
        async with self.ss() as session:
            await session.merge(project, options=[joinedload(Project.users_responded_to_project),
                                                  joinedload(Project.users_invited_in_project)])
            await session.commit()
            return project

    async def get_project_by_id(self, id: int) -> Project | None:
        async with self.ss() as session:
            project = await session.scalar(select(Project).where(Project.id == id).options(joinedload(
                    Project.users_responded_to_project),joinedload(Project.users_invited_in_project))
            )
            return project

    async def get_all_projects(self) -> list[Project]:
        async with self.ss() as session:
            projects = await session.execute(select(Project).options(joinedload(
                    Project.users_responded_to_project),joinedload(Project.users_invited_in_project))
            )
            return projects.scalars().unique().all()

    async def get_user_projects(self, user_id: int) -> list[Project]:
        async with self.ss() as session:
            projects = await session.execute(select(Project).where(Project.owner_id == user_id).options(joinedload(
                    Project.users_responded_to_project),joinedload(Project.users_invited_in_project))
            )
            return projects.scalars().unique().all()

    async def get_users_by_role(self, role: str) -> list[User]:
        async with self.ss() as session:
            users = await session.execute(select(User).where(User.role == role))
            return users.scalars().all()

    async def create_project(self, project: Project) -> Project:
        async with self.ss() as session:
            session.add(project)
            await session.commit()
            return project

    async def get_experts(self) -> list[User]:
        async with self.ss() as session:
            experts = await session.execute(select(User).where(User.is_expert == True))
            return experts.scalars().unique().all()

    async def get_folders_by_user(self, owner: int) -> list[AchievementFolder]:
        async with self.ss() as session:
            folders = await session.execute(select(AchievementFolder).where(AchievementFolder.owner_id == owner))
            return folders.scalars().all()

    async def get_folder_by_id(self, folder_id: int) -> AchievementFolder:
        async with self.ss() as session:
            folder = await session.scalar(select(AchievementFolder).where(AchievementFolder.id == folder_id))
            return folder
    async def get_achievements_by_folder(self, folder_id: int) -> list[Achievement]:
        async with self.ss() as session:
            achievements = await session.execute(select(Achievement).where(Achievement.folder_id == folder_id))
            return achievements.scalars().all()

    async def create_folder(self, folder: AchievementFolder) -> AchievementFolder:
        async with self.ss() as session:
            session.add(folder)
            await session.commit()
            return folder

    async def update_folder(self, folder: AchievementFolder) -> AchievementFolder:
        async with self.ss() as session:
            await session.merge(folder)
            await session.commit()
            return folder

    async def get_achievement_by_id(self, achievement_id: int) -> Achievement:
        async with self.ss() as session:
            achievement = await session.scalar(select(Achievement).where(Achievement.id == achievement_id))
            return achievement

    async def delete_folder(self, folder_id: int) -> None:
        async with self.ss() as session:
            folder = await session.scalar(select(AchievementFolder).where(AchievementFolder.id == folder_id))
            await session.delete(folder)
            await session.commit()
            return folder

    async def delete_achievement(self, achievement_id: int) -> None:
        async with self.ss() as session:
            achievement = await session.scalar(select(Achievement).where(Achievement.id == achievement_id))
            await session.delete(achievement)
            await session.commit()
            return achievement

    async def create_achievement(self, achievement: Achievement) -> Achievement:
        async with self.ss() as session:
            session.add(achievement)
            await session.commit()
            return achievement

    async def update_achievement(self, achievement: Achievement) -> Achievement:
        async with self.ss() as session:
            await session.merge(achievement)
            await session.commit()
            return achievement

    async def change_password(self, user: User, new_password: str) -> User:
        async with self.ss() as session:
            user.password = passlib.hash.argon2.hash(new_password)
            await session.merge(user)
            await session.commit()
            return user

    async def delete_project(self, project_id: int) -> None:
        async with self.ss() as session:
            project = await session.scalar(select(Project).where(Project.id == project_id))
            await session.delete(project)
            await session.commit()
            return project

    async def select_where_responded(self, user_id: int) -> None:
        async with self.ss() as session:
            # choose projects where user is in users_responded_to_project
            projects = await session.execute(select(Project).where(Project.users_responded_to_project.any(
                    UserInvited.user_id == user_id)))
            return projects.scalars().all()