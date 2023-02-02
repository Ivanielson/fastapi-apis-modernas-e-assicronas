from typing import Optional, Any, List
from fastapi import FastAPI, HTTPException, status, Response, Path, Query
from fastapi import Depends
# from fastapi.responses import JSONResponse
from models import Course, courses
from time import sleep


def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados...')
        sleep(1)


app = FastAPI(
    title='Api de Cursos da Geek University',
    version='0.0.1',
    description='Uma API para colocar em prática os estudos do FastAPI',
)


@app.get(
    '/courses',
    description='Retorna todos os cursos cadastrados ou uma lista vazia',
    summary='Retorna todos os Cursos',
    status_code=status.HTTP_200_OK,
    response_model=List[Course],
    response_description='Cursos encontrados com sucesso.'
)
async def get_all_courses(db: Any = Depends(fake_db)):
    return courses


@app.get(
    '/courses/{id}',
    status_code=status.HTTP_200_OK,
    description='Retorna o curso com ID passado na URL (Se existir)',
    summary='Retorna um curso',
    response_model=Course,
    response_description='Curso encontrado com sucesso.'
)
async def get_course_by_id(id: int = Path(
        default=None,
        title='ID do curso',
        description='Deve ser entre 1 e 2',
        gt=0,
        lt=3), db: Any = Depends(fake_db)):
    try:
        for course in courses:
            if course.id == id:
                return course
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID não encontrado")


@app.post(
    '/courses',
    status_code=status.HTTP_201_CREATED,
    description='Cadastra um novo curso com as informações passa no body',
    summary='Cria um curso',
    response_model=Course,
    response_description='Curso cadastrado com sucesso.'
)
async def create_course(course: Course, db: Any = Depends(fake_db)):
    ids = [value.id for value in courses]
    if course.id not in ids:
        courses.append(course)
        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um curso registrado com esse o ID {course.id}.")


@app.put(
    '/courses/{id}',
    status_code=status.HTTP_200_OK,
    description='Atualiza as informaçẽos do curso de acordo com o ID passado',
    summary='Atualiza um curso',
    response_model=Course,
    response_description='Curso atualizado com sucesso.'
)
async def update_course(course: Course, id: int, db: Any = Depends(fake_db)):
    for value in courses:
        if id == value.id:
            index = courses.index(value)
            courses[index] = course
            return course
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com ID {id}.")


@app.delete(
    '/courses/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Deleta um curso cadastrado de acordo com ID passado',
    summary='Deleta um curso',
    response_description='Curso deletado com sucesso.'
)
async def delete_course(id: int, db: Any = Depends(fake_db)):
    for value in courses:
        if id == value.id:
            index = courses.index(value)
            del courses[index]
            # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com ID {id}"
        )


@app.get(
    '/sum',
    description='Faz a soma dos números passados',
    summary='Retorna a soma dos números'
)
async def sum(a: int, b: int, c: Optional[int] = None):
    sum_number = a + b
    if c:
        sum_number += c
    return {"Result": sum_number}


@app.get(
    '/divide',
    description='Faz a divisão do primeiro número passado pelo segundo',
    summary='Retorna a divisão de dois números'
)
async def divide(
    num1: int = Query(default=None, gt=0),
    num2: int = Query(default=None, gt=0)
):
    div = num1 / num2
    return {"result": div}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
