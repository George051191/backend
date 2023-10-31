import pytest

def test_get_me(test_app, login_headers):
    response = test_app.get("/user/me", headers=login_headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("email") == "testtest@ya.ru"

def test_update_me(test_app, login_headers):
    update_json = {
        "socialNetworks": {
            "vk": "https://vk.com/id1",
            "telegram": "https://t.me/id1",
            "ok": "https://ok.ru/id1",
        }
    }
    response = test_app.patch("/user/me", headers=login_headers, json=update_json)
    assert response.status_code == 200
    assert response.json().get("id") == 1
