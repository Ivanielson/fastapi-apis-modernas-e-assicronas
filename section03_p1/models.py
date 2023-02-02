from typing import Optional

from pydantic import BaseModel


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int


courses = [
    Course(
        id=1,
        title="Programação para Leigos",
        classes=112,
        hours=58
    ),
    Course(
        id=2,
        title="Algoritmos e Lógica de Programação",
        classes=87,
        hours=67
    )
]
