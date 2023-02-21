from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def create_article(
    article: ArticleSchema,
    user_logged_in: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    new_article: ArticleModel = ArticleModel(
        title=article.title,
        description=article.description,
        url_source=article.url_source,
        user_id=user_logged_in.id
    )

    db.add(new_article)
    await db.commit()

    return new_article


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ArticleSchema])
async def get_all_articles(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=ArticleSchema)
async def get_article_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article
        else:
            raise HTTPException(detail="Artigo não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ArticleSchema)
async def update_article(
    id: int,
    article: ArticleSchema,
    user_logged_in: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article_update: ArticleModel = result.scalars().unique().one_or_none()

        if article_update:
            article_update.title = article.title
            article_update.description = article.description
            article_update.url_source = article.url_source                
            if article_update.user_id != user_logged_in.id:
                article_update.user_id = user_logged_in.id
            
            await session.commit()
            return article_update
        else:
            raise HTTPException(detail="Artigo não encontrado.", status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_article_by_id(
    id: int,
    user_logged_in: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article_del: ArticleModel = result.scalars().unique().one_or_none()

        if article_del:
            if article_del.user_id != user_logged_in.id and not user_logged_in.is_admin:
                raise HTTPException(detail="Permisão negada.", status_code=status.HTTP_401_UNAUTHORIZED)
            else:
                await session.delete(article_del)
                await session.commit()
                return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail="Artigo não encontrado.", status_code=status.HTTP_404_NOT_FOUND)
            