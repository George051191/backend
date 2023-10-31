import os
import platform

import fastapi
import sqlalchemy.ext.asyncio
import sentry_sdk

from src.database import Database
from src.services.login.app import router as login_router
from src.services.users.app import router as user_router
from src.services.projects.app import router as project_router
from src.services.achievements.app import router as achievement_router
from src.services.files.app import router as file_router
from src.services.utils.app import router as utils_router
from src.utils import JWTAbc, JWT
import src.settings
from fastapi.middleware.cors import CORSMiddleware


def on_startup():
    pass


def on_shutdown():
    pass


def get_app():
    app = fastapi.FastAPI()
    if platform.system() != "Darwin":
        sentry_sdk.init(
        dsn="https://0ffee971779d675912f44609b23d0e40@o4506036847902720.ingest.sentry.io/4506036849082368",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0
    )
    app.include_router(login_router, prefix="/login")
    app.include_router(user_router, prefix="/user")
    app.include_router(project_router, prefix="/projects")
    app.include_router(achievement_router, prefix="/achievements")
    app.include_router(file_router, prefix="/files")
    app.include_router(utils_router, prefix="/utils")

    settings = src.settings.Settings()

    engine = sqlalchemy.ext.asyncio.create_async_engine(settings.DB_URL)
    sessionmaker = sqlalchemy.ext.asyncio.async_sessionmaker(
        bind=engine, expire_on_commit=False
    )
    app.dependency_overrides[JWTAbc] = lambda: JWT(
        "563a4c0b3a91189b822a309555c12ff570db87ba9972b8a75f1609153bbcf80b", "HS256"
    )
    app.dependency_overrides[Database] = lambda: Database(sessionmaker)
    # TODO: move secret for JWT to settings and secrets

    # app.on_event("startup")(on_startup)
    # app.on_event("shutdown")(on_shutdown)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

    # app.dependency_overrides[fastapi.Depends] = fastapi.Depends


app = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.__main__:app", host="0.0.0.0")
