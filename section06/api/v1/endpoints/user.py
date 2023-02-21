from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import authenticate, create_token_access


router = APIRouter()


@router.get('/logged', response_model=UserSchemaBase)
def get_logged(user_logged_in: UserModel = Depends(get_current_user)):
    return user_logged_in


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        name=user.name,
        last_name=user.last_name,
        email=user.email,
        password=generate_password_hash(user.password),
        is_admin=user.is_admin
    )
    async with db as session:
        try:
            session.add(new_user)
            await session.commit()
            return new_user
        except IntegrityError:
            raise HTTPException(detail="Já existe um usuário cadastrado com o e-mail informado.", status_code=status.HTTP_409_CONFLICT)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserSchemaBase])
async def get_all_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserSchemaArticles)
async def get_user_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=UserSchemaBase)
async def update_user(id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_up: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_up:
            if user.name:
                user_up.name = user.name
            if user.last_name:
                user_up.last_name = user.last_name
            if user.email:
                user_up.email = user.email
            if user.password:
                user_up.password = generate_password_hash(user.password)
            if user.is_admin:
                user_up.is_admin = user.is_admin
            await session.commit()
            return user_up
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_user_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == id)
        result = await session.execute(query)
        user_del: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_del:
            await session.delete(user_del)
            await session.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Usuário não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Dados de acesso incorretos.")

    return JSONResponse(content={"access_token": create_token_access(sub=user.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)

