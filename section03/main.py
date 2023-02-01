from fastapi import FastAPI, HTTPException, status, Response, Path, Query
# from fastapi.responses import JSONResponse
from models import Course


app = FastAPI()


courses = {
    1: {
        "id": 1,
        "title": "Programação para Leigos",
        "classes": 112,
        "hours": 58
    },
    2: {
        "id": 2,
        "title": "Algoritmos e Lógica de Programação",
        "classes": 87,
        "hours": 67
    }
}


@app.get('/courses', status_code=status.HTTP_200_OK)
async def get_all_courses():
    return courses


@app.get('/courses/{id}', status_code=status.HTTP_200_OK)
async def get_course_by_id(id: int = Path(
        default=None,
        title='ID do curso',
        description='Deve ser entre 1 e 2',
        gt=0,
        lt=3)):
    try:
        course = courses[id]
        return course
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID não encontrado")


@app.post('/courses', status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    if course.id not in courses:
        courses[course.id] = course
        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um curso registrado com esse o ID {course.id}.")


@app.put('/courses/{id}', status_code=status.HTTP_200_OK)
async def update_course(course: Course, id: int):
    if id in courses:
        courses[id] = course
        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com ID {id}.")


@app.delete('/courses/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int):
    if id in courses:
        del courses[id]
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não existe um curso com ID {id}"
        )


@app.get('/sum')
async def sum(a: int, b: int, c: int):
    sum_number = a + b + c
    return {"Result": sum_number}


@app.get('/divide')
async def divide(
    num1: int = Query(default=None, gt=0),
    num2: int = Query(default=None, gt=0)
):
    div = num1 / num2
    return {"result": div}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
