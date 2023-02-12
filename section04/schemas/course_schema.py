from typing import Optional
from pydantic import BaseModel as SCBaseModel


class CourseSchema(SCBaseModel):
    id: Optional[int]
    title: str
    classes: int
    hours: int

    class Config:
        orm_mode = True
