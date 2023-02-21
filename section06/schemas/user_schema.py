from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.article_schema import ArticleSchema


class UserSchemaBase(BaseModel):
    id: Optional[int]
    name: str
    last_name: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True


class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticles(UserSchemaBase):
    articles: Optional[list[ArticleSchema]]


class UserSchemaUpdate(UserSchemaBase):
    name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
