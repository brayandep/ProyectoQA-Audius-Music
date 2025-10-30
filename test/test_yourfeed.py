def test_your_feed(page_with_session):
    page = page_with_session
    page.goto("https://audius.co/feed")

    # Verifica que se muestre la sección "Trending Tracks"
    assert page.locator("text=Trending Tracks").is_visible()

    # (Opcional) Captura una screenshot
    page.screenshot(path="feed.png")
