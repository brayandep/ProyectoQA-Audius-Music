# pages/yourfeed_page.py
from playwright.sync_api import Page, Locator, expect
from config.settings import FEED_URL

class YourFeedPage:
    def __init__(self, page: Page):
        self.page = page

        # ==== LOCATORS ====
        self.title: Locator = page.get_by_role("heading", name="Your Feed")
        self.card: Locator = page.locator('[data-testid="trackTile"], [class*="track"]').first
        self.play_button: Locator = page.locator('button[aria-label*="Play"]').first
        self.repost_button: Locator = page.locator('button[aria-label*="Repost"]').first
        self.favorite_button: Locator = page.locator('button[aria-label*="Favorite"]').first
        self.more_options_button: Locator = page.locator('button[aria-label*="More options"], button:has(svg)')
        self.add_playlist_option: Locator = page.get_by_text("Add to Playlist")
        self.new_playlist_option: Locator = page.get_by_text("New Playlist")
        self.share_option: Locator = page.get_by_text("Share")
        self.direct_message_option: Locator = page.get_by_text("Direct Message")
        self.embedded_option: Locator = page.get_by_text("Embed")
        self.copy_link_option: Locator = page.get_by_text("Copy Link")

        # Elementos esperados tras acciones
        self.mini_player: Locator = page.locator('[class*="miniPlayer"], [data-testid*="playerBar"]')
        self.confirm_toast: Locator = page.locator('text=added to playlist, copied, etc')
        self.embed_modal: Locator = page.locator('[role="dialog"] >> text=Embed')
        self.search_dm: Locator = page.locator('input[placeholder*="Search"], [aria-label*="Search"]')

    # ==== MÉTODOS ====
    def open(self):
        self.page.goto(FEED_URL)
        expect(self.title).to_be_visible(timeout=10000)

    def play_from_card(self):
        self.card.click()
        expect(self.mini_player).to_be_visible(timeout=10000)

    def click_repost(self):
        self.repost_button.click()
        expect(self.repost_button).to_have_attribute("aria-pressed", "true")

    def open_more_options(self):
        self.more_options_button.click()
        expect(self.page.get_by_text("Add to Playlist")).to_be_visible()

    def create_playlist(self):
        self.add_playlist_option.click()
        self.new_playlist_option.click()
        expect(self.confirm_toast).to_be_visible(timeout=8000)

    def click_favorite(self):
        self.favorite_button.click()
        expect(self.favorite_button).to_have_attribute("aria-pressed", "true")

    def click_share(self):
        self.share_option.click()
        expect(self.direct_message_option).to_be_visible()

    def click_direct_message(self):
        self.direct_message_option.click()
        expect(self.search_dm).to_be_visible(timeout=8000)

    def click_embed(self):
        self.embedded_option.click()
        expect(self.embed_modal).to_be_visible(timeout=8000)

    def click_copy_link(self):
        self.copy_link_option.click()
        expect(self.confirm_toast).to_be_visible(timeout=8000)
