from playwright.sync_api import expect
from config.settings import FEED_URL
def test_your_feed(page_with_session):
    page = page_with_session
    page.goto(FEED_URL)
   
    try:
        expect(page.locator("text=Your Feed")).to_be_visible(timeout=15000)
        print("✅ El módulo 'Your Feed' se cargó correctamente.")
    except AssertionError:
        page.screenshot(path="feed_debug.png", full_page=True)
        print("⚠️ No se encontró 'Your Feed'. Se guardó feed_debug.png para inspeccionar.")
        raise
