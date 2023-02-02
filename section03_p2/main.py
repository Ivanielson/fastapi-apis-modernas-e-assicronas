from fastapi import FastAPI
from routes import course_router, user_router


app = FastAPI()

app.include_router(course_router.router, tags=['Courses'])
app.include_router(user_router.router, tags=['Users'])


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True, reload=True)
