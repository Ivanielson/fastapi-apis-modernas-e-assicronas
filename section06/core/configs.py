from typing import List
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = os.environ["DB_URL"]
    DBBaseModel = declarative_base()
    JWT_SECRET: str = "0neJWKOTihh4zm-qTYqflt2dzy01zSMOTUJOiLys96U"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
