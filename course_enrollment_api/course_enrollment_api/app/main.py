from fastapi import FastAPI
from app.routes import user_routes, course_routes, enrollment_routes

app = FastAPI(title="Course Enrollment Management API")

app.include_router(user_routes.router)
app.include_router(course_routes.router)
app.include_router(enrollment_routes.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Course Enrollment Management API"}
