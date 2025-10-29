from playwright.sync_api import BrowserType, BrowserContext
from config.settings import settings

def launch_browser(pw) -> BrowserContext:
    browser_type: BrowserType = getattr(pw, settings.browser)
    browser = browser_type.launch(headless=settings.headless)
    context = browser.new_context(
        viewport={"width": settings.viewport_width, "height": settings.viewport_height}
    )
    return context
