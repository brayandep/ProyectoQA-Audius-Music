# pages/base_page.py
from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def expect_visible(self, locator: str):
        expect(self.page.locator(locator)).to_be_visible()

    def fill(self, locator: str, value: str):
        self.page.locator(locator).fill(value)  # sin .clear()
