from typing import Dict
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment

class DataStore:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.courses: Dict[int, Course] = {}
        self.enrollments: Dict[int, Enrollment] = {}
        self.user_counter = 1
        self.course_counter = 1
        self.enrollment_counter = 1

    def clear(self):
        self.users.clear()
        self.courses.clear()
        self.enrollments.clear()
        self.user_counter = 1
        self.course_counter = 1
        self.enrollment_counter = 1

datastore = DataStore()
