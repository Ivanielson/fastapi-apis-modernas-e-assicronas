from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.curso_model import CursoModel
from schemas.course_schema import CourseSchema
from core.deps import get_session


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def create_course(curso: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CursoModel(curso)
    db.add(new_course)
    await db.commit()

    return new_course


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CourseSchema])
async def get_all_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        courses: List[CursoModel] = result.scalars().all()
        return courses