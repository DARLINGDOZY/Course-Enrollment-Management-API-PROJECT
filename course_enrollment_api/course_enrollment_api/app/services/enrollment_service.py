from app.storage.datastore import datastore
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate, EnrollmentDelete
from fastapi import HTTPException, status

class EnrollmentService:
    @staticmethod
    def enroll_student(data: EnrollmentCreate) -> Enrollment:
        # Check if user exists and is a student
        user = datastore.users.get(data.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        # Check role from request
        if data.role != "student" or user.role != "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can enroll themselves")

        # Check if course exists
        course = datastore.courses.get(data.course_id)
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

        # Check if already enrolled
        for enr in datastore.enrollments.values():
            if enr.user_id == data.user_id and enr.course_id == data.course_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already enrolled in this course")

        enr_id = datastore.enrollment_counter
        new_enr = Enrollment(id=enr_id, user_id=data.user_id, course_id=data.course_id)
        datastore.enrollments[enr_id] = new_enr
        datastore.enrollment_counter += 1
        return new_enr

    @staticmethod
    def deregister_student(data: EnrollmentDelete):
        user = datastore.users.get(data.user_id)
        if not user or user.role != "student" or data.role != "student":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can deregister themselves")

        enr_id_to_delete = None
        for eid, enr in datastore.enrollments.items():
            if enr.user_id == data.user_id and enr.course_id == data.course_id:
                enr_id_to_delete = eid
                break
        
        if enr_id_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
        
        del datastore.enrollments[enr_id_to_delete]

    @staticmethod
    def get_student_enrollments(user_id: int):
        user = datastore.users.get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return [enr for enr in datastore.enrollments.values() if enr.user_id == user_id]

    @staticmethod
    def get_all_enrollments():
        return list(datastore.enrollments.values())

    @staticmethod
    def get_course_enrollments(course_id: int):
        if course_id not in datastore.courses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        return [enr for enr in datastore.enrollments.values() if enr.course_id == course_id]

    @staticmethod
    def force_deregister(user_id: int, course_id: int, role: str):
        if role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
        
        enr_id_to_delete = None
        for eid, enr in datastore.enrollments.items():
            if enr.user_id == user_id and enr.course_id == course_id:
                enr_id_to_delete = eid
                break
        
        if enr_id_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
        
        del datastore.enrollments[enr_id_to_delete]
