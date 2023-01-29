from typing import Optional

from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int
