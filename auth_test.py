from fastapi.testclient import TestClient

from app.main import app

 

client = TestClient(app)

 

def test_login_success():

    r = client.post("/auth/login", json={"username": "alice", "password": "alicepass"})

    assert r.status_code == 200

    assert "access_token" in r.json()

 

def test_login_wrong_password():

    r = client.post("/auth/login", json={"username": "alice", "password": "wrong"})

    assert r.status_code == 401

 

def test_login_nonexistent_user():

    r = client.post("/auth/login", json={"username": "ghost", "password": "x"})

    assert r.status_code == 401

 

def test_me_requires_token():

    r = client.get("/me")

    assert r.status_code == 401

 

def test_me_with_valid_token():

    login = client.post("/auth/login", json={"username": "alice", "password": "alicepass"})

    token = login.json()["access_token"]

    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    assert r.status_code == 200

    assert r.json()["user"] == "alice"

 

def test_admin_route_blocks_non_admin():

    login = client.post("/auth/login", json={"username": "bob", "password": "bobpass"})

    token = login.json()["access_token"]

    r = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token}"})

    assert r.status_code == 403

 

def test_admin_route_allows_admin():

    login = client.post("/auth/login", json={"username": "alice", "password": "alicepass"})

    token = login.json()["access_token"]

    r = client.get("/admin/dashboard", headers={"Authorization": f"Bearer {token}"})

    assert r.status_code == 200