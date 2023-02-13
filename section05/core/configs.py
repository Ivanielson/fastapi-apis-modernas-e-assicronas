from pydantic import BaseSettings
import os
from dotenv import load_dotenv
load_dotenv()


USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']
DB = os.environ['DB_NAME']

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@localhost:5432/{DB}"

    class Config:
        case_sensitive = True


settings: Settings = Settings()
