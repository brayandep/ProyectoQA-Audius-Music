import pytest
import allure
from playwright.sync_api import expect
from pages.yourfeed_page import YourFeedPage

# ============================================================
# 🎧 TEST FUNCIONALES DEL MÓDULO "YOUR FEED" (Audius Music)
# ============================================================

@allure.feature("Your Feed")
@allure.story("Visualización inicial del módulo")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC001 - Verificar título 'Your Feed' visible correctamente")
@pytest.mark.functional
def test_TC001_titulo_your_feed(page_with_session):
    """Verifica que el título 'Your Feed' se muestre correctamente."""
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir el módulo Your Feed"):
        feed.open()
        feed.handle_notification_modal()

    with allure.step("Verificar visibilidad del título"):
        expect(feed.title).to_be_visible(timeout=10000)
        allure.attach(page_with_session.screenshot(), name="Pantalla_YourFeed", attachment_type=allure.attachment_type.PNG)
        print("✅ Título 'Your Feed' visible correctamente.")


@allure.feature("Your Feed")
@allure.story("Reproducción de música")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC002 - Reproducir canción desde una tarjeta y mostrar mini-player")
@pytest.mark.functional
def test_TC002_reproduccion_en_mini_player(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir Your Feed y reproducir desde una tarjeta"):
        feed.open()
        feed.handle_notification_modal()
        feed.play_from_card()

    with allure.step("Verificar mini-reproductor visible"):
        expect(feed.mini_player).to_be_visible(timeout=8000)
        allure.attach(page_with_session.screenshot(), name="Mini_Player", attachment_type=allure.attachment_type.PNG)
        print("✅ Mini reproductor visible después de hacer clic en la tarjeta.")


@allure.feature("Your Feed")
@allure.story("Interacciones sociales")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC003 - Marcar y desmarcar Repost correctamente")
@pytest.mark.functional
def test_TC003_marcar_repost(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir Your Feed y marcar Repost"):
        feed.open()
        feed.handle_notification_modal()
        feed.click_repost()
        allure.attach(page_with_session.screenshot(), name="Repost_Marcado", attachment_type=allure.attachment_type.PNG)
        print("✅ Repost marcado correctamente.")


@allure.feature("Your Feed")
@allure.story("Menú de opciones de canción")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC004 - Desplegar menú de opciones correctamente")
@pytest.mark.functional
def test_TC004_desplegar_opciones(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir opciones de canción (3 puntos)"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        allure.attach(page_with_session.screenshot(), name="Menu_Opciones", attachment_type=allure.attachment_type.PNG)
        print("✅ Menú de opciones desplegado correctamente.")


@allure.feature("Your Feed")
@allure.story("Gestión de playlist")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC005 - Crear una nueva playlist desde el menú")
@pytest.mark.functional
def test_TC005_crear_playlist(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir menú de opciones y crear playlist"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.create_playlist()
        allure.attach(page_with_session.screenshot(), name="Playlist_Creada", attachment_type=allure.attachment_type.PNG)
        print("✅ Playlist creada y mensaje de confirmación mostrado.")


@allure.feature("Your Feed")
@allure.story("Marcado de favoritos")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC006 - Marcar canción como favorita correctamente")
@pytest.mark.functional
def test_TC006_marcar_favorito(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Marcar canción como favorita"):
        feed.open()
        feed.handle_notification_modal()
        feed.click_favorite()
        allure.attach(page_with_session.screenshot(), name="Favorito", attachment_type=allure.attachment_type.PNG)
        print("✅ Canción marcada como favorita correctamente.")


@allure.feature("Your Feed")
@allure.story("Compartir contenido")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC007 - Mostrar opciones de compartir correctamente")
@pytest.mark.functional
def test_TC007_mostrar_opciones_de_compartir(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir menú y mostrar opciones de compartir"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        allure.attach(page_with_session.screenshot(), name="Opciones_Compartir", attachment_type=allure.attachment_type.PNG)
        print("✅ Opciones de compartir mostradas correctamente.")


@allure.feature("Your Feed")
@allure.story("Mensajes directos")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC008 - Abrir buscador de mensajes directos desde Share")
@pytest.mark.functional
def test_TC008_abrir_direct_message(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir buscador de mensajes directos"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        feed.click_direct_message()
        allure.attach(page_with_session.screenshot(), name="Direct_Message", attachment_type=allure.attachment_type.PNG)
        print("✅ Buscador de mensajes directos visible correctamente.")


@allure.feature("Your Feed")
@allure.story("Integración externa (Embed)")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC009 - Abrir modal 'Embed' correctamente")
@pytest.mark.functional
def test_TC009_abrir_modal_embed(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir modal Embed"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_embed()
        allure.attach(page_with_session.screenshot(), name="Modal_Embed", attachment_type=allure.attachment_type.PNG)
        print("✅ Modal 'Embed' mostrado correctamente.")


@allure.feature("Your Feed")
@allure.story("Compartir canciones")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Copiar link de canción correctamente")
@pytest.mark.functional
def test_TC010_copiar_link(page_with_session):
    feed = YourFeedPage(page_with_session)

    with allure.step("Copiar link desde opciones de compartir"):
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        feed.click_copy_link()
        allure.attach(page_with_session.screenshot(), name="Copy_Link", attachment_type=allure.attachment_type.PNG)
        print("✅ Enlace copiado y mensaje de confirmación visible.")
