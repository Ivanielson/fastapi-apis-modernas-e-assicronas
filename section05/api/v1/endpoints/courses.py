from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.course_model import CourseModel
from core.deps import get_session


# Bypass warning SQLModel select
from sqlmodel.sql.expression import Select, SelectOfScalar

SelectOfScalar.inherit_cache = True
Select.inherit_cache = True
# Fim Bypass


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseModel)
async def create_course(course: CourseModel, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(title=course.title, classes=course.classes, hours=course.hours)
    db.add(new_course)
    await db.commit()
    return new_course


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CourseModel])
async def get_all_courses(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()
        return courses
