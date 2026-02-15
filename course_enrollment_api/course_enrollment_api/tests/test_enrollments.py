from fastapi import status

def test_enroll_student_success(client):
    # Setup: Create user and course
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    
    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] == 1

def test_enroll_student_forbidden_role(client):
    client.post("/users", json={"name": "A1", "email": "a1@ex.com", "role": "admin"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    
    response = client.post("/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student" # Trying to enroll an admin as a student
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_duplicate_enrollment(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    response = client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_deregister_success(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    
    response = client.request("DELETE", "/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_deregister_not_found(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    response = client.request("DELETE", "/enrollments", json={
        "user_id": 1,
        "course_id": 1,
        "role": "student"
    })
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_get_student_enrollments(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    
    response = client.get("/students/1/enrollments")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
