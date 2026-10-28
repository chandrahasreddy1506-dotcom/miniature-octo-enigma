import os

import requests


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = float(os.getenv("API_TEST_TIMEOUT", "8"))


def test_home_page_available():
    response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
    assert response.status_code == 200
    assert "Talk & Solve" in response.text


def test_register_page_available():
    response = requests.get(f"{BASE_URL}/register/", timeout=TIMEOUT)
    assert response.status_code == 200


def test_login_page_available():
    response = requests.get(f"{BASE_URL}/login/", timeout=TIMEOUT)
    assert response.status_code == 200


def test_issue_detail_page_available_or_not_found():
    response = requests.get(f"{BASE_URL}/issues/1/", timeout=TIMEOUT)
    assert response.status_code in {200, 404}
