from typing import Optional

from pydantic import BaseModel, validator


class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int

    @validator('title')
    def validates_title(cls, value: str):
        words = value.split(" ")
        if len(words) < 3:
            raise ValueError("O campo 'title' deve ter pelo menos 3 palvras")
        return value

    @validator('classes')
    def validates_classes(cls, value: int):
        if value <= 12:
            raise ValueError(
                "O campo 'classes' deve ter um valor maior que 12"
            )
        return value

    @validator('hours')
    def validates_hours(cls, value: int):
        if value <= 10:
            raise ValueError(
                "O campo 'hours' deve ter um valor maior que 10"
            )
        return value


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
