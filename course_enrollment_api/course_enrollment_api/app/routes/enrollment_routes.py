from fastapi import APIRouter, status, Query
from typing import List
from app.schemas.enrollment import EnrollmentCreate, EnrollmentDelete, EnrollmentResponse
from app.services.enrollment_service import EnrollmentService
from app.utils.role_checker import check_role

router = APIRouter(tags=["Enrollments"])

@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_student(data: EnrollmentCreate):
    return EnrollmentService.enroll_student(data)

@router.delete("/enrollments", status_code=status.HTTP_204_NO_CONTENT)
async def deregister_student(data: EnrollmentDelete):
    EnrollmentService.deregister_student(data)
    return None

@router.get("/students/{user_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_student_enrollments(user_id: int):
    return EnrollmentService.get_student_enrollments(user_id)

@router.get("/enrollments", response_model=List[EnrollmentResponse])
async def get_all_enrollments(role: str = Query(...)):
    check_role(role, "admin")
    return EnrollmentService.get_all_enrollments()

@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_course_enrollments(course_id: int, role: str = Query(...)):
    check_role(role, "admin")
    return EnrollmentService.get_course_enrollments(course_id)

@router.delete("/admin/enrollments", status_code=status.HTTP_204_NO_CONTENT)
async def admin_force_deregister(user_id: int = Query(...), course_id: int = Query(...), role: str = Query(...)):
    EnrollmentService.force_deregister(user_id, course_id, role)
    return None
