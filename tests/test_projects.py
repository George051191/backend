def test_create_public_project(test_app, login_headers):
    json = {"name":            "test", "idea": "test", "status": "test", "stage": "test", "achievements": [],
        "year":                "2021", "division": "test", "images": [], "file": "test", "description": "test",
        "team":                [], "experts": [], "descriptionFullness": 0, "isPublished": True, }
    response = test_app.post("/projects/create", headers=login_headers, json=json)
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("name") == "test"
    assert response.json().get("idea") == "test"
    assert response.json().get("status") == "test"
    assert response.json().get("stage") == "test"
    assert response.json().get("achievements") == []
    assert response.json().get("year") == "2021"
    assert response.json().get("division") == "test"
    assert response.json().get("images") == []
    assert response.json().get("file") == "test"
    assert response.json().get("description") == "test"
    assert response.json().get("team") == []
    assert response.json().get("experts") == []
    assert response.json().get("descriptionFullness") == 0
    assert response.json().get("isPublished") == True
    assert response.json().get("createdAt") is not None


def test_create_private_project(test_app, login_headers):
    json = {"name": "test"}
    response = test_app.post("/projects/create", headers=login_headers, json=json)
    assert response.status_code == 200
    assert response.json().get("id") == 2
    assert response.json().get("isPublished") == False
    assert response.json().get("createdAt") is not None
    # we don't check all fields because it's the same as in test_create_private_project


def test_get_projects(test_app, login_headers):
    response = test_app.get("/projects/all", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1  # because one is private
    assert response.json()[0].get("id") == 1

def test_update_project(test_app, login_headers):
    json = {"projectId": 2, "name": "test2", "idea": "test2", "status": "test2", "stage": "test2", "achievements": [],
        "year":                "2021", "division": "test2", "images": [], "file": "test2", "description": "test2",
        "team":                [], "experts": [], "descriptionFullness": 0, "isPublished": True, }
    response = test_app.patch("/projects/update", headers=login_headers, json=json)
    assert response.status_code == 200
    assert response.json().get("id") == 2
    assert response.json().get("name") == "test2"
    assert response.json().get("idea") == "test2"
    assert response.json().get("status") == "test2"
    assert response.json().get("stage") == "test2"
    assert response.json().get("achievements") == []
    assert response.json().get("year") == "2021"
    assert response.json().get("division") == "test2"
    assert response.json().get("images") == []
    assert response.json().get("file") == "test2"
    assert response.json().get("description") == "test2"
    assert response.json().get("team") == []
    assert response.json().get("experts") == []
    assert response.json().get("descriptionFullness") == 0
    assert response.json().get("isPublished") == True
    assert response.json().get("createdAt") is not None

def test_get_my_projects(test_app, login_headers):
    response = test_app.get("/projects/my", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2
    ids = [p.get("id") for p in response.json()]
    ids.sort()
    assert ids == [1, 2]

def test_publish_project(test_app, login_headers):
    response = test_app.patch("/projects/publish", headers=login_headers, json={"publish": True, "projectId": 1})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("isPublished") == True

    response = test_app.get("/projects/all", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = test_app.patch("/projects/publish", headers=login_headers, json={"publish": False, "projectId": 1})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("isPublished") == False

    response = test_app.get("/projects/all", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_invite_user(test_app, login_headers):
    response = test_app.patch("/projects/invite", headers=login_headers, json={"projectId": 1, "userId": 1})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("usersInvitedInProject")[0].get("id") == 1

def test_invited(test_app, login_headers):
    response = test_app.get("/projects/requestsProjects", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("id") == 1
def test_requests_my(test_app, login_headers):
    response = test_app.get("/projects/requestsMy", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()["experts"]) == 1
    assert response.json()["experts"][0].get("id") == 1

def test_respond_to_project(test_app, login_headers):
    response = test_app.patch("/projects/respond", headers=login_headers, json={"projectId": 1})
    assert response.status_code == 200
    assert response.json().get("id") == 1
    assert response.json().get("usersRespondedToProject")[0].get("id") == 1

def test_share_contact(test_app, login_headers):
    response = test_app.post("/projects/shareContacts", headers=login_headers, json={"projectId": 1, "shown" : True})
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

def test_delete_project(test_app, login_headers):
    response = test_app.delete("/projects/1", headers=login_headers)
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    response = test_app.get("/projects/my", headers=login_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get("id") == 2