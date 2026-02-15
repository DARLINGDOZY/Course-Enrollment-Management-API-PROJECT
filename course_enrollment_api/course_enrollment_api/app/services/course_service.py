from app.storage.datastore import datastore
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.utils.validators import validate_unique_course_code
from fastapi import HTTPException, status

class CourseService:
    @staticmethod
    def create_course(course_data: CourseCreate) -> Course:
        validate_unique_course_code(course_data.code)
        course_id = datastore.course_counter
        new_course = Course(
            id=course_id,
            title=course_data.title,
            code=course_data.code
        )
        datastore.courses[course_id] = new_course
        datastore.course_counter += 1
        return new_course

    @staticmethod
    def get_all_courses():
        return list(datastore.courses.values())

    @staticmethod
    def get_course_by_id(course_id: int) -> Course:
        course = datastore.courses.get(course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        return course

    @staticmethod
    def update_course(course_id: int, course_data: CourseUpdate) -> Course:
        course = CourseService.get_course_by_id(course_id)
        
        if course_data.code is not None:
            validate_unique_course_code(course_data.code, exclude_id=course_id)
            course.code = course_data.code
        
        if course_data.title is not None:
            course.title = course_data.title
            
        return course

    @staticmethod
    def delete_course(course_id: int):
        if course_id not in datastore.courses:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course with ID {course_id} not found"
            )
        del datastore.courses[course_id]
        
        # Optionally remove associated enrollments
        enrollments_to_delete = [
            eid for eid, enr in datastore.enrollments.items()
            if enr.course_id == course_id
        ]
        for eid in enrollments_to_delete:
            del datastore.enrollments[eid]
