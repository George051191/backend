from fastapi.testclient import TestClient
import pytest


def test_failed_login(test_app: TestClient):
    response = test_app.post(
        "/login/login",
        json={
            "email": "a@ya.ru",
            "password": "123456",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": {"message": "Invalid credentials"}}

def test_weak_password(test_app: TestClient):
    response = test_app.post(
        "/login/register",
        json={
            "email": "a@ya.ru",
            "password": "123456",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": {"message": "Password does not match requirements"}}

def test_register(test_app: TestClient):
    response = test_app.post(
        "/login/register",
        json={
            "email": "a@ya.ru",
            "password": "nfhreb123ui",
        },
    )
    assert response.status_code == 200

def test_already_exists(test_app: TestClient):
    response = test_app.post(
        "/login/register",
        json={
            "email": "a@ya.ru",
            "password": "nfhreb123ui",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": {"message": "User already exists"}}

def test_login(test_app: TestClient):
    response = test_app.post(
        "/login/login",
        json={
            "email": "a@ya.ru",
            "password": "nfhreb123ui",
        },
    )
    assert response.status_code == 200
    assert response.json().get("jwt_token")


def test_change_password(test_app: TestClient):
    login = test_app.post(
        "/login/login",
            json={
                "email":    "a@ya.ru",
                "password": "nfhreb123ui",
            },
    )
    token = login.json().get("jwt_token")
    response = test_app.patch(
        "/login/change-password",
        json={
            "oldPassword": "nfhreb123ui",
            "newPassword": "nfhreb123ui2",
        },
        headers={"Authorization": f"Bearer {token}"},)
    assert response.status_code == 200
    assert response.json() == {"success": True}

    response = test_app.post(
        "/login/login",
            json={
                "email":"a@ya.ru",
                "password":"nfhreb123ui2",
            },
    )
    assert response.status_code == 200
    assert response.json().get("jwt_token")

