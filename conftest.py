import os
import pytest
from playwright.sync_api import sync_playwright
from config.browsers import launch_browser
from config.settings import settings

@pytest.fixture(scope="session")
def playwright_context():
    with sync_playwright() as pw:
        context = launch_browser(pw)
        yield context
        context.close()

@pytest.fixture(scope="function")
def page(playwright_context):
    page = playwright_context.new_page()
    page.set_default_timeout(10000)
    yield page
    # captura en fallo
    if hasattr(page, "_test_failed") and page._test_failed:
        os.makedirs("test-results/screens", exist_ok=True)
        page.screenshot(path=f"test-results/screens/{page._test_failed}.png")
    page.close()

# Hook para marcar fallos y nombrar screenshots
def pytest_runtest_makereport(item, call):
    if "page" in item.fixturenames and call.when == "call":
        page = item.funcargs["page"]
        if call.excinfo is not None:
            page._test_failed = item.name
