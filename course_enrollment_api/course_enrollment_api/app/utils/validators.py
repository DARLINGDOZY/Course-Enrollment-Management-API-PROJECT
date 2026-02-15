from fastapi import HTTPException, status
from app.storage.datastore import datastore

def validate_unique_course_code(code: str, exclude_id: int = None):
    for course in datastore.courses.values():
        if course.code == code and (exclude_id is None or course.id != exclude_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Course code '{code}' already exists"
            )
