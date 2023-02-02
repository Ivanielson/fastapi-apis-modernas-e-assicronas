from fastapi import APIRouter


router = APIRouter()


@router.get('/api/v1/courses')
async def get_all_courses():
    return {"info": "Todos os cursos"}