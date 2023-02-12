from core.configs import settings
from sqlalchemy import Column, Integer, String


class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(100))
    classes: int = Column(Integer)
    hours: int = Column(Integer)