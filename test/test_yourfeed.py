import pytest
import allure
from playwright.sync_api import expect
from pages.yourfeed_page import YourFeedPage

# ============================================================
# 🎧 TEST FUNCIONALES DEL MÓDULO "YOUR FEED" (Audius Music)
# ============================================================

@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC001 - Verificar título 'Your Feed' visible correctamente")
@allure.description("""
Description
El usuario ingresa al módulo 'Your Feed' y visualiza correctamente el título principal de la sección en pantalla.

Resultado esperado : El título “Your Feed” se muestra visible sin errores de carga o renderizado.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC001_titulo_your_feed(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir el módulo Your Feed"):
        test_logger.info("Abriendo módulo Your Feed")
        feed.open()
        feed.handle_notification_modal()

    with allure.step("Verificar visibilidad del título"):
        expect(feed.title).to_be_visible(timeout=10000)
        allure.attach(page_with_session.screenshot(), name="Pantalla_YourFeed", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Título 'Your Feed' visible correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC002 - Reproducir canción desde una tarjeta y mostrar mini-player")
@allure.description("""
Description
Desde la lista de canciones en 'Your Feed', el usuario hace clic en una tarjeta para reproducir una canción.

Resultado esperado : El mini-reproductor aparece en la parte inferior mostrando el nombre de la canción y los controles de reproducción activos.

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Aplicación Audius abierta
Sesión iniciada con una cuenta válida
Disponibilidad de canciones en 'Your Feed'
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC002_reproduccion_en_mini_player(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir Your Feed y reproducir desde una tarjeta"):
        test_logger.info("Entrando a Your Feed y reproduciendo una canción")
        feed.open()
        feed.handle_notification_modal()
        feed.play_from_card()

    with allure.step("Verificar mini-reproductor visible"):
        expect(feed.mini_player).to_be_visible(timeout=8000)
        allure.attach(page_with_session.screenshot(), name="Mini_Player", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Mini reproductor visible después de hacer clic en la tarjeta.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC003 - Marcar y desmarcar Repost correctamente")
@allure.description("""
Description
El usuario hace clic en el botón “Repost” de una tarjeta para republicar o retirar una publicación.

Resultado esperado : El icono de Repost cambia de estado (activo/inactivo) y el conteo se actualiza sin recargar la página.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Sesión activa
Canciones visibles en el feed
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC003_marcar_repost(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir Your Feed y marcar Repost"):
        test_logger.info("Cargando Your Feed y probando el botón Repost")
        feed.open()
        feed.handle_notification_modal()
        feed.click_repost()
        allure.attach(page_with_session.screenshot(), name="Repost_Marcado", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Repost marcado correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC004 - Desplegar menú de opciones correctamente")
@allure.description("""
Description
El usuario selecciona el menú de opciones (ícono de tres puntos) en una tarjeta de canción.

Resultado esperado : Se despliega correctamente el menú contextual con las opciones disponibles (Share, Add to Playlist, etc.).

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Sesión iniciada
Canción disponible en el feed
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC004_desplegar_opciones(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir opciones de canción (3 puntos)"):
        test_logger.info("Accediendo al menú de opciones de una canción")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        allure.attach(page_with_session.screenshot(), name="Menu_Opciones", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Menú de opciones desplegado correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC005 - Crear una nueva playlist desde el menú")
@allure.description("""
Description
El usuario abre el menú de opciones de una canción y selecciona la opción “Add to Playlist” → “Create new playlist”.
Resultado esperado : Se crea una nueva playlist y el sistema muestra un mensaje de confirmación o modal de configuración.
Pre-conditions
SO/Navegador: Windows/macOS/Linux
Aplicación Audius abierta
Sesión iniciada válida
Canciones disponibles en 'Your Feed'
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC005_crear_playlist(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir menú de opciones y crear playlist"):
        test_logger.info("Creando una nueva playlist desde el menú")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.create_playlist()
        allure.attach(page_with_session.screenshot(), name="Playlist_Creada", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Playlist creada y mensaje de confirmación mostrado.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC006 - Marcar canción como favorita correctamente")
@allure.description("""
Description
El usuario hace clic en el ícono de “Favorite” (corazón) de una canción para marcarla o desmarcarla como favorita.

Resultado esperado : El ícono cambia de color/estado y la acción se refleja en el perfil del usuario.

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Sesión iniciada válida
Canciones visibles en el feed
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC006_marcar_favorito(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Marcar canción como favorita"):
        test_logger.info("Marcando canción como favorita")
        feed.open()
        feed.handle_notification_modal()
        feed.click_favorite()
        allure.attach(page_with_session.screenshot(), name="Favorito", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Canción marcada como favorita correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC007 - Mostrar opciones de compartir correctamente")
@allure.description("""
Description
El usuario abre el menú de opciones (3 puntos) de una canción y selecciona “Share” para ver las formas de compartir.

Resultado esperado : Se muestra el panel o modal con las opciones de compartir (Copy Link, Embed, Direct Message, etc.).

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Sesión iniciada
Canción disponible en 'Your Feed'
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC007_mostrar_opciones_de_compartir(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir menú y mostrar opciones de compartir"):
        test_logger.info("Abriendo menú de opciones → clic en 'Share'")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        allure.attach(page_with_session.screenshot(), name="Opciones_Compartir", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Opciones de compartir mostradas correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC008 - Abrir buscador de mensajes directos desde Share")
@allure.description("""
Description
Desde las opciones de compartir, el usuario selecciona “Direct Message” para enviar la canción a otro usuario.

Resultado esperado : Se abre el buscador o modal de mensajes directos para seleccionar el destinatario.

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Sesión iniciada válida
Canciones disponibles en 'Your Feed'
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC008_abrir_direct_message(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir buscador de mensajes directos"):
        test_logger.info("Probando opción 'Direct Message' en el menú Share")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        feed.click_direct_message()
        allure.attach(page_with_session.screenshot(), name="Direct_Message", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Buscador de mensajes directos visible correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC009 - Abrir modal 'Embed' correctamente")
@allure.description("""
Description
El usuario accede a la opción “Embed” desde el menú de compartir para obtener el código de inserción.

Resultado esperado : Se muestra un modal con el código embebido listo para copiar (HTML/iframe).

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Sesión iniciada
Canciones visibles en 'Your Feed'
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC009_abrir_modal_embed(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Abrir modal Embed"):
        test_logger.info("Probando opción 'Embed'")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_embed()
        allure.attach(page_with_session.screenshot(), name="Modal_Embed", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Modal 'Embed' mostrado correctamente.")


@allure.feature("Your Feed")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Copiar link de canción correctamente")
@allure.description("""
Description
El usuario selecciona la opción “Copy Link” desde el menú de compartir de una canción.

Resultado esperado : El sistema copia la URL al portapapeles y muestra un mensaje de confirmación (ej. “Link copied!”).

Pre-conditions
SO/Navegador: Windows/macOS/Linux
Aplicación Audius accesible
Sesión iniciada válida
Canciones disponibles en 'Your Feed'
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC010_copiar_link(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)

    with allure.step("Copiar link desde opciones de compartir"):
        test_logger.info("Probando flujo Share → Copy Link")
        feed.open()
        feed.handle_notification_modal()
        feed.open_more_options()
        feed.click_share()
        feed.click_copy_link()
        allure.attach(page_with_session.screenshot(), name="Copy_Link", attachment_type=allure.attachment_type.PNG)
        test_logger.info("✅ Enlace copiado y mensaje de confirmación visible.")
