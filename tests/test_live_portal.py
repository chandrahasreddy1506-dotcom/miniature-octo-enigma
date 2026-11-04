import os
import time
from playwright.sync_api import Page, expect

BASE_URL = "https://chandu1.pythonanywhere.com"
TEST_USERNAME = "kiran"
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "Kiran@123")


def test_01_live_security_redirect(page: Page):
    """Verify unauthenticated visitors redirect to the login screen."""
    page.goto(BASE_URL)
    expect(page).to_have_url(f"{BASE_URL}/accounts/login/?next=/")
    expect(page.locator("button[type='submit']")).to_be_visible()


def test_02_live_citizen_login(page: Page):
    """Verify login works on PythonAnywhere and loads the dashboard."""
    page.goto(f"{BASE_URL}/accounts/login/")
    page.locator("input[name='username']").fill(TEST_USERNAME)
    page.locator("input[name='password']").fill(TEST_PASSWORD)
    page.locator("button[type='submit']").click()

    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("text=Talk & Solve")).to_be_visible()


def test_03_live_submit_grievance_modal(page: Page):
    """Open modal, submit a civic issue, and verify it renders in the table."""
    page.goto(f"{BASE_URL}/accounts/login/")
    page.locator("input[name='username']").fill(TEST_USERNAME)
    page.locator("input[name='password']").fill(TEST_PASSWORD)
    page.locator("button[type='submit']").click()

    # Open modal
    page.locator("button:has-text('+ Report Grievance')").first.click()
    modal_title = page.locator("#grievanceModalLabel")
    expect(modal_title).to_be_visible()

    # Fill form fields
    unique_title = f"Live CI Check {int(time.time())}"
    page.locator("#grievanceModal input[name='title']").fill(unique_title)
    page.locator("#grievanceModal select[name='department']").select_option("Electricity & Lighting")
    page.locator("#grievanceModal input[name='location']").fill("Automated Pipeline Sector 1")
    page.locator("#grievanceModal textarea[name='description']").fill("Automated end-to-end regression validation run.")

    # Submit and verify
    page.locator("#grievanceModal button:has-text('Submit Complaint')").click()
    expect(modal_title).not_to_be_visible()
    expect(page.locator(f"table tbody td:has-text('{unique_title}')")).to_be_visible()