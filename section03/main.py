from fastapi import FastAPI, HTTPException, status

from models import Curso


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
async def get_course_by_id(id: int):
    try:
        course = courses[id]
        return course
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID não encontrado")


@app.post('/courses', status_code=status.HTTP_201_CREATED)
async def create_course(course: Curso):
    if course.id not in courses:
        courses[course.id] = course
        return course
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um curso registrado com esse o ID {course.id}.")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
