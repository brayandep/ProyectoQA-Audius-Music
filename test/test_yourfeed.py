# test/test_yourfeed.py
import pytest
from pages.yourfeed_page import YourFeedPage

@pytest.mark.functional
def test_TC001_titulo_your_feed(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    assert feed.title.is_visible(), "❌ No se encontró el título 'Your Feed'."


@pytest.mark.functional
def test_TC002_reproduccion_en_mini_player(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.play_from_card()
    assert feed.mini_player.is_visible(), "❌ No se mostró el mini reproductor."


@pytest.mark.functional
def test_TC003_marcar_repost(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.click_repost()


@pytest.mark.functional
def test_TC004_desplegar_opciones(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()


@pytest.mark.functional
def test_TC005_crear_playlist(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()
    feed.create_playlist()


@pytest.mark.functional
def test_TC006_marcar_favorito(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.click_favorite()


@pytest.mark.functional
def test_TC007_mostrar_opciones_de_compartir(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()
    feed.click_share()


@pytest.mark.functional
def test_TC008_abrir_direct_message(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()
    feed.click_share()
    feed.click_direct_message()


@pytest.mark.functional
def test_TC009_abrir_modal_embed(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()
    feed.click_embed()


@pytest.mark.functional
def test_TC010_copiar_link(page_with_session):
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.open_more_options()
    feed.click_copy_link()
