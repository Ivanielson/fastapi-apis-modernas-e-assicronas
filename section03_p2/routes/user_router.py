from fastapi import APIRouter


router = APIRouter()


@router.get('/api/v1/users')
async def get_all_users():
    return {"info": "Todos os usuários"}