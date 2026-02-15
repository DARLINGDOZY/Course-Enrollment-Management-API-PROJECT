from fastapi import APIRouter, status, Query, Depends
from typing import List, Optional
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services.course_service import CourseService
from app.utils.role_checker import check_role

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("", response_model=List[CourseResponse])
async def get_courses():
    return CourseService.get_all_courses()

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int):
    return CourseService.get_course_by_id(course_id)

@router.post("", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(course_data: CourseCreate, role: str = Query(...)):
    check_role(role, "admin")
    return CourseService.create_course(course_data)

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(course_id: int, course_data: CourseUpdate, role: str = Query(...)):
    check_role(role, "admin")
    return CourseService.update_course(course_id, course_data)

@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, role: str = Query(...)):
    check_role(role, "admin")
    CourseService.delete_course(course_id)
    return None
