from fastapi import status

def test_create_user_success(client):
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "student"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["role"] == "student"

def test_create_user_invalid_email(client):
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "invalid-email",
        "role": "student"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_user_invalid_role(client):
    response = client.post("/users", json={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "manager"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_get_users(client):
    client.post("/users", json={"name": "U1", "email": "u1@ex.com", "role": "admin"})
    client.post("/users", json={"name": "U2", "email": "u2@ex.com", "role": "student"})
    
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2

def test_get_user_by_id(client):
    client.post("/users", json={"name": "U1", "email": "u1@ex.com", "role": "admin"})
    
    response = client.get("/users/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "U1"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
