# Course Enrollment Management API

A RESTful API built with FastAPI for managing users, courses, and enrollments.

## Features
- User Management (Student/Admin roles)
- Course Management (Admin-only creation/update/deletion)
- Enrollment System (Student self-enrollment, Admin oversight)
- In-memory storage (no database required)
- Comprehensive test suite

## Requirements
- Python 3.8+
- FastAPI
- Pydantic
- Pytest

## Setup and Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Access the API documentation:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Running Tests

Run the following command from the root directory:
```bash
pytest -v
```

## API Endpoints Summary

### User Management
- `POST /users`: Create user
- `GET /users`: List users
- `GET /users/{id}`: Get user details

### Course Management
- `GET /courses`: List courses (Public)
- `GET /courses/{id}`: Get course details (Public)
- `POST /courses?role=admin`: Create course (Admin)
- `PUT /courses/{id}?role=admin`: Update course (Admin)
- `DELETE /courses/{id}?role=admin`: Delete course (Admin)

### Enrollment Management
- `POST /enrollments`: Student enrollment (Body: user_id, course_id, role="student")
- `DELETE /enrollments`: Student deregistration (Body: user_id, course_id, role="student")
- `GET /students/{user_id}/enrollments`: List student's enrollments
- `GET /enrollments?role=admin`: List all enrollments (Admin)
- `GET /courses/{course_id}/enrollments?role=admin`: List enrollments for a course (Admin)
- `DELETE /admin/enrollments?role=admin&user_id={uid}&course_id={cid}`: Force deregister (Admin)
