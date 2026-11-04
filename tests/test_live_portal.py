import os
import pytest
from playwright.sync_api import Page, expect

BASE_URL = "https://chandu1.pythonanywhere.com"

def test_01_live_security_redirect(page: Page):
    page.goto(f"{BASE_URL}/")
    expect(page).to_have_url(f"{BASE_URL}/accounts/login/?next=/")

def test_02_live_citizen_login(page: Page):
    password = os.environ.get("TEST_PASSWORD", "Kiran@123")
    page.goto(f"{BASE_URL}/accounts/login/")
    page.fill('input[name="username"]', "kiran")
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    expect(page).to_have_url(f"{BASE_URL}/")

def test_03_live_submit_grievance_modal(page: Page):
    password = os.environ.get("TEST_PASSWORD", "Kiran@123")
    page.goto(f"{BASE_URL}/accounts/login/")
    page.fill('input[name="username"]', "kiran")
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')

    page.click('button:has-text("Raise Issue"), button:has-text("New Issue"), [data-bs-target="#newIssueModal"]')
    page.fill('input[name="title"]', "Automated CI/CD Sanity Check")
    page.fill('textarea[name="description"]', "Playwright pipeline verification entry.")
    page.click('button[type="submit"]:has-text("Submit"), input[type="submit"]')

    response = page.request.get(f"{BASE_URL}/export/csv/")
    assert response.status == 200