# test/test_yourfeed.py
import pytest
from pages.yourfeed_page import YourFeedPage
from playwright.sync_api import expect

# ============================================================
# 🧩 TEST FUNCTIONALES DEL MÓDULO YOUR FEED (Audius Music)
# ============================================================

@pytest.mark.functional
def test_TC001_titulo_your_feed(page_with_session):
    """Verifica que el título 'Your Feed' se muestre correctamente."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    expect(feed.title).to_be_visible(timeout=10000)
    print("✅ Título 'Your Feed' visible correctamente.")


@pytest.mark.functional
def test_TC002_reproduccion_en_mini_player(page_with_session):
    """Verifica que al hacer clic en la tarjeta se muestre el mini reproductor."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.play_from_card()
    expect(feed.mini_player).to_be_visible(timeout=8000)
    print("✅ Mini reproductor visible después de hacer clic en la tarjeta.")


@pytest.mark.functional
def test_TC003_marcar_repost(page_with_session):
    """Verifica que el botón 'Repost' pueda cambiar a unrepost o sucesivamente."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.click_repost()
    print("✅ Repost marcado correctamente.")


@pytest.mark.functional
def test_TC004_desplegar_opciones(page_with_session):
    """Verifica que al hacer clic en los tres puntos se desplieguen las opciones."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    print("✅ Menú de opciones desplegado correctamente.")


@pytest.mark.run
def test_TC005_crear_playlist(page_with_session):
    """Verifica que se pueda crear una nueva playlist desde el menú."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    feed.create_playlist()
    print("✅ Playlist creada y mensaje de confirmación mostrado.")


@pytest.mark.functional
def test_TC006_marcar_favorito(page_with_session):
    """Verifica que el botón 'Favorite' pueda marcarse correctamente."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.click_favorite()
    print("✅ Canción marcada como favorita correctamente.")


@pytest.mark.functional
def test_TC007_mostrar_opciones_de_compartir(page_with_session):
    """Verifica que al hacer clic en 'Share' se muestren las opciones de compartir."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    feed.click_share()
    print("✅ Opciones de compartir mostradas correctamente.")


@pytest.mark.functional
def test_TC008_abrir_direct_message(page_with_session):
    """Verifica que al hacer clic en 'Direct Message' se abra el buscador."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    feed.click_share()
    feed.click_direct_message()
    print("✅ Buscador de mensajes directos visible correctamente.")


@pytest.mark.functional
def test_TC009_abrir_modal_embed(page_with_session):
    """Verifica que al hacer clic en 'Embed' se abra el modal correspondiente."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    feed.click_embed()
    print("✅ Modal 'Embed' mostrado correctamente.")


@pytest.mark.functional
def test_TC010_copiar_link(page_with_session):
    """Verifica que al hacer clic en 'Copy Link' se muestre un mensaje de confirmación."""
    feed = YourFeedPage(page_with_session)
    feed.open()
    feed.handle_notification_modal() 
    feed.open_more_options()
    feed.click_copy_link()
    print("✅ Enlace copiado y mensaje de confirmación visible.")
