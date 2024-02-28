from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_users():
    response = client.get("/user/")
    assert response.status_code == 200
    assert response.json() == []
 
def test_other_routes():
    response = client.get("/random")
    assert response.status_code == 404

def test_create_user():
    response = client.post("/user/siginup", json={
        "name": "mario",
        "username": "mario",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "User created successfully"}

def test_create_same_user():
    response = client.post("/user/siginup", json={
        "name": "mario",
        "username": "mario",
        "password": "1234"
    })
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "Username already exists"}

def test_login_user():
    response = client.post("/user/login", json={
        "username": "mario",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "access_token" in response.json()

def test_login_user_invalid_password():
    response = client.post("/user/login", json={
        "username": "test",
        "password": "test1"
    })
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "Invalid username or password"}

def test_login_user_invalid_username():
    response = client.post("/user/login", json={
        "username": "test1",
        "password": "test"
    })
    assert response.status_code == 400
    assert response.json() == {"status": "error", "message": "Invalid username or password"}

def test_create_test_case():
    token = client.post("/user/login", json={
        "username": "mario",
        "password": "1234"
    }).json()["access_token"]
    response = client.post("/testcase/", json={
        "name": "test",
        "description": "test"
    }, headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Test case created successfully"}

def test_create_execution_result():
    token = client.post("/user/login", json={
        "username": "mario",
        "password": "1234"
    }).json()["access_token"]
    response = client.post("/executionresult/", json={
        "test_case_id": 1,
        "test_asset": "test",
        "result": "test"
    }, headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Execution result created successfully"}

def test_read_execution_results():
    response = client.get("/executionresult/")
    assert response.status_code == 200
    assert response.json() == [{
        "id": 1,
        "test_case_id": {
            "id": 1,
            "name": "test",
            "description": "test"
        },
        "test_asset": "test",
        "result": "test",
        "user_id": {
            "id": 1,
            "name": "mario",
            "username": "mario"
        }
    }]

def delete_test_case():
    token = client.post("/user/login", json={
        "username": "test",
        "password": "test"
    }).json()["access_token"]
    response = client.delete("/testcase/1", headers={"Authorization": "Bearer " + token})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Test case deleted successfully"}

