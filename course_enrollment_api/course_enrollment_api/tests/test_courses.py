from fastapi import status

def test_create_course_admin_success(client):
    response = client.post("/courses?role=admin", json={
        "title": "Python Programming",
        "code": "PY101"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["code"] == "PY101"

def test_create_course_forbidden(client):
    response = client.post("/courses?role=student", json={
        "title": "Python Programming",
        "code": "PY101"
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_duplicate_course_code(client):
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    response = client.post("/courses?role=admin", json={"title": "C2", "code": "CS101"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]

def test_get_courses_public(client):
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    response = client.get("/courses")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

def test_update_course_admin(client):
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    response = client.put("/courses/1?role=admin", json={"title": "C1 Updated"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "C1 Updated"

def test_delete_course_admin(client):
    client.post("/courses?role=admin", json={"title": "C1", "code": "CS101"})
    response = client.delete("/courses/1?role=admin")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    get_resp = client.get("/courses/1")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
