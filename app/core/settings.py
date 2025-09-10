from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REPO_PATH: str
    FILE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
