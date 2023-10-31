import pytest

def test_find_msu_upper(test_app):
    response = test_app.get("/utils/uni-search?name=МГУ")
    assert response.status_code == 200
    assert "МГУ" in response.json()[0]

def test_find_msu_lower_case(test_app):
    response = test_app.get("/utils/uni-search?name=мгу")
    assert response.status_code == 200
    assert "МГУ" in response.json()[0]