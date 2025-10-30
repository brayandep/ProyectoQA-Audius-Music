import pytest
from config.settings import settings

@pytest.mark.upload
def test_upload_track_minimo(page):
    # partimos ya autenticados por storage_state
    page.goto(f"{settings.base_url}/upload")

    # TODO: reemplazar por tus selectores
    page.set_input_files('input[type="file"]', "resources/audio/track-demo.mp3")
    page.fill('input[name="trackName"]', "Mi Canción Demo")
    page.fill('textarea[name="description"]', "Descripción corta")
    page.click('button:has-text("Publish"), button:has-text("Upload")')

    # confirmar algún toast/redirect
    # expect(page.locator(".toast-success")).to_be_visible()
