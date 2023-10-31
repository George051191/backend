from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DB_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"
    FILES_PATH: str = "/Users/alex/PycharmProjects/poprojecteam/backend/files/"

