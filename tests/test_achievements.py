import io
import tempfile

import pytest

def test_get_achievements(test_app, login_headers):
    response = test_app.get("/achievements", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_create_folder(test_app, login_headers):
    response = test_app.post("/achievements", headers=login_headers, json={"name": "test"})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("name") == "test"
    assert response.json().get("createdAt") is not None

def test_get_folder(test_app, login_headers):
    response = test_app.get("/achievements/1", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_update_folder(test_app, login_headers):
    response = test_app.patch("/achievements/1", headers=login_headers, json={"name": "test2"})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("name") == "test2"
    assert response.json().get("createdAt") is not None

def test_create_blank_achievement(test_app, login_headers):
    # send form with name and description
    response = test_app.post("/achievements/1", json={"name": "test", "description": "test", "files": [], "date": "2021-01-01"},
    headers=login_headers)
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("name") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("date") == "2021-01-01"
    assert response.json().get("createdAt") is not None
    assert len(response.json().get("files")) == 0

# def test_create_file__achievement(test_app, login_headers):
#     with tempfile.TemporaryDirectory() as tempdir:
#         file = f"{tempdir}/test.txt"
#         with open(file, "w") as f:
#             f.write("test")
#         file = open(file, "rb")
#
#
#         response = test_app.post("/achievements/1", data={"name": "test", "description": "test"},
#                                  files=[("uploaded_files", file)], headers=login_headers)
#         assert response.status_code == 200
#         assert response.json().get("id") == 2
#         assert response.json().get("name") == "test"
#         assert response.json().get("description") == "test"
#         assert len(response.json().get("files")) == 1
#
#     def test_get_file(response):
#         response = test_app.get(f"/files/{response.json().get('files')[0]}", headers=login_headers)
#         assert response.status_code == 200
#         assert response.content == b"test"
#
#     test_get_file(response)

# def test_change_achievement(test_app, login_headers):
#     with tempfile.TemporaryDirectory() as tempdir:
#         file = f"{tempdir}/test.txt"
#         with open(file, "w") as f:
#             f.write("test2")
#         file = open(file, "rb")
#
#         response = test_app.patch("/achievements/1/1", headers=login_headers, data={"name": "test2", "description":
#             "test2"},files=[("uploaded_files", file)])
#         assert response.status_code == 200
#         assert response.json().get("id") == 1
#         assert response.json().get("name") == "test2"
#         assert response.json().get("description") == "test2"
#
#     def test_get_changed_file(response):
#         response = test_app.get(f"/files/{response.json().get('files')[0]}", headers=login_headers)
#         assert response.status_code == 200
#         assert response.content == b"test2"
#
#     test_get_changed_file(response)

def test_delete_achievement(test_app, login_headers):
    response = test_app.delete("/achievements/1/1", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # response = test_app.delete("/achievements/1/2", headers=login_headers)
    # assert response.status_code == 200
    # assert response.json() == {"success": True}

    response = test_app.get("/achievements/1", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_delete_folder(test_app, login_headers):
    response = test_app.delete("/achievements/1", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == {"success": True}

    response = test_app.get("/achievements", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == []

def test_delete_folder_cascade(test_app, login_headers):
    response = test_app.post("/achievements", headers=login_headers, json={"name": "test"})
    assert response.status_code == 200
    assert response.json().get("id") == 2

    response = test_app.post("/achievements/2", headers=login_headers, json={"name": "test", "description": "test", "files": [], "date": "2021-01-01"})
    assert response.status_code == 200

    response = test_app.delete("/achievements/2", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == {"success": True}