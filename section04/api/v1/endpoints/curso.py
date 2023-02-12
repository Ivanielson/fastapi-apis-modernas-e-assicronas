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
    new_course = CursoModel(title=curso.title, classes=curso.classes, hours=curso.hours)
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


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_course(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        course: CourseSchema = result.scalar_one_or_none()

        if course:
            return course
        else:
            raise HTTPException(detail="Curso não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def update_course(id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        course_update = result.scalar_one_or_none()

        if course_update:
            course_update.title = course.title
            course_update.classes = course.classes
            course_update.hours = course.hours
            await session.commit()
            return course_update
        else:
            raise HTTPException(detail="Curso não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == id)
        result = await session.execute(query)
        course_delete = result.scalar_one_or_none()

        if course_delete:
            await session.delete(course_delete)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Curso não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
