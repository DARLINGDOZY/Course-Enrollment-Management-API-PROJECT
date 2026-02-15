from fastapi import status

def test_admin_get_all_enrollments(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    
    response = client.get("/enrollments?role=admin")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

def test_admin_get_course_enrollments(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    
    response = client.get("/courses/1/enrollments?role=admin")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

def test_admin_force_deregister(client):
    client.post("/users", json={"name": "S1", "email": "s1@ex.com", "role": "student"})
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    client.post("/enrollments", json={"user_id": 1, "course_id": 1, "role": "student"})
    
    response = client.delete("/admin/enrollments?role=admin&user_id=1&course_id=1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify enrollment is gone
    check_resp = client.get("/enrollments?role=admin")
    assert len(check_resp.json()) == 0

def test_admin_force_deregister_forbidden(client):
    response = client.delete("/admin/enrollments?role=student&user_id=1&course_id=1")
    assert response.status_code == status.HTTP_403_FORBIDDEN
