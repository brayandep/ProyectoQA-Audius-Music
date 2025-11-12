# test/test_myprofile.py
import pytest
import allure
from pages.yourfeed_page import YourFeedPage
from pages.myprofile_page import MyProfilePage

# ===========================================================
# TEST FUNCIONALES DEL MÓDULO "MY PROFILE" (Audius Music)
# Flujo: Your Feed → clic en avatar → Perfil → acciones
# ===========================================================

@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC001 - Abrir modal de Folowlers")
@allure.description("""
Description
Desde Your Feed, el usuario abre su Perfil y toca el contador/enlace de “Followers” para visualizar el listado en un modal.

Resultado esperado : Se muestra el modal de Followers con el conteo y la lista (puede estar vacía), es desplazable y se puede cerrar sin cambiar de página.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox actualizados
Aplicación web Audius accesible
Sesión iniciada con una cuenta válida
Perfil del usuario existente (con o sin followers)
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC001_abrir_modal_followers(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)


    with allure.step("Abrir el perfil del usuario"):
        
        profile.open_profile()
        feed.handle_notification_modal()

    with allure.step("Abrir el modal de Followers"):
        test_logger.info("Abriendo modal 'Followers'")
        profile.open_followers_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC002 - Abrir modal de Following")
@allure.description("""
Description
Desde el Perfil del usuario, se toca el contador/enlace de “Following” para visualizar el listado en un modal.

Resultado esperado : Se muestra el modal de Following con el conteo y la lista (puede estar vacía), es desplazable y se puede cerrar sin afectar la navegación.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario existente (con o sin following)
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC002_abrir_modal_following(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)   
    profile = MyProfilePage(page_with_session)

    with allure.step("Abrir el perfil del usuario"):
        profile.open_profile()
        feed.handle_notification_modal()

    with allure.step("Abrir modal Following"):
        test_logger.info("Abriendo modal 'Following'")
        profile.open_following_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC003 - Abrir modal de compartir perfil")
@allure.description("""
Description
Desde el Perfil, el usuario abre el menú/acción de “Share” para obtener opciones de compartir el perfil (enlace/copiar/compartir nativo).

Resultado esperado : Se muestra el modal de compartir con un enlace del perfil y controles de copia/compartición; el modal se puede cerrar sin recargar la página.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC003_abrir_modal_share_profile(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Abrir perfil y compartir"):

        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_share_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC004 - No guardar nombre vacío en track")
@allure.description("""
Description
Desde el Perfil, se edita un track y se intenta guardar dejando el campo “Name/Track” vacío.

Resultado esperado : El sistema bloquea el guardado y muestra un mensaje de validación (p. ej., “Your track must have a name.”). No se persisten cambios.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Existe al menos un track del usuario para editar
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC004_no_guardar_nombre_vacio(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar editar un track con nombre vacío"):
        test_logger.info("Abriendo edición de track y probando nombre vacío")
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_track_for_edit()
        profile.try_empty_song_name()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC005 - No guardar nombre con solo espacios")
@allure.description("""
Description
En edición de track, el usuario ingresa únicamente espacios en el campo “Name/Track” e intenta guardar.

Resultado esperado : Se bloquea el guardado y se muestra validación equivalente a nombre vacío.
Nota: Caso marcado como xfail por bug conocido (actualmente acepta espacios).

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Track del usuario disponible para edición
""")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="Permite espacios en blanco en campo Name de track")
def test_TC005_no_guardar_nombre_con_espacios(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar guardar con nombre de solo espacios"):
        test_logger.info("Probando nombre con solo espacios")

        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_track_for_edit()
        profile.try_blank_song_name()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC006 - No guardar imagen vacía en track")
@allure.description("""
Description
En edición de track, el usuario intenta guardar sin seleccionar/adjuntar imagen (artwork) cuando el flujo la requiere.

Resultado esperado : El sistema impide guardar y muestra una validación acorde (no se persisten cambios ni se cierra el modal de edición).

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Track del usuario disponible para edición
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC006_guardar_foto_perfil_de_track_vacia(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Verificar guardar sin imagen de perfil"):
        test_logger.info("Intentando guardar track sin seleccionar imagen")

        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_track_for_edit()
        profile.try_save_empty_profile_picture()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC007 - Editar descripción con caracteres válidos")
@allure.description("""
Description
Desde el Perfil, el usuario entra en modo edición y actualiza la descripción con texto válido (se aceptan letras, números, signos y emojis).

Resultado esperado : La descripción se actualiza y persiste; se refleja en la vista de perfil sin errores ni recarga completa.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC007_editar_descripcion_con_caracteres_validos(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar descripción con texto válido"):
        test_logger.info("Editando descripción del perfil")
 
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_edit_mode()
        profile.editar_descripcion("Perfil actualizado automáticamente desde Playwright QA 🧠")
        profile.guardar_cambios()
        test_logger.info("Descripción guardada correctamente")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC008 - Editar nombre del artista con datos válidos")
@allure.description("""
Description
En edición de Perfil, el usuario actualiza el campo “Artista” con un nombre válido dentro de los límites permitidos.

Resultado esperado : El nombre de artista se guarda y se muestra en el encabezado del perfil sin mensajes de error.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.smoke
@pytest.mark.integration
def test_TC008_editar_el_campo_Nombre_artista_con_datos_validos(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar campo Artista con nombre válido"):
        test_logger.info("Editando nombre de artista → 'QA Tester Automation'")
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_edit_mode()
        profile.editar_nombre("QA Tester Automation")
        profile.guardar_cambios()
        test_logger.info("Nombre de artista guardado")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC009 - No superar 30 caracteres en campo Artista")
@allure.description("""
Description
El usuario intenta ingresar más de 30 caracteres en el campo “Artista” e intenta guardar.

Resultado esperado : Se bloquea el guardado y se muestra un mensaje de validación (p. ej., “Fix errors to continue.”).
Nota: Caso xfail por comportamiento actual: se corta el texto sin mensaje.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.functional
@pytest.mark.integration
@pytest.mark.xfail(reason="No se muestra mensaje al superar los 30 caracteres; el sistema solo corta el texto")
def test_TC009_Verificar_que_al_editar_el_campo_Artista_no_Supere_los_30_caracteres_mostrando_un_mensaje(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar ingresar más de 30 caracteres"):
        test_logger.info("Probando validación de longitud >30 en 'Artista'")
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_edit_mode()
        profile.editar_nombre("LaamistadesunarelaciónafectivaentredosomáspersonasLaamistadesunarelaciónafectivaentredosomáspersonas")
        profile.guardar_cambios()

    with allure.step("Validar mensaje de error mostrado"):
        test_logger.info("Verificando mensaje 'Fix errors to continue.'")
        assert profile.validar_mensaje("Fix errors to continue."), "❌ No se mostró el mensaje esperado"


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Permitir mínimo 1 caracter en campo Artista")
@allure.description("""
Description
El usuario ingresa un solo carácter en el campo “Artista” y guarda los cambios.

Resultado esperado : El cambio se guarda correctamente y se actualiza el nombre en el perfil sin mostrar errores.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC010_Verificar_que_al_editar_el_campo_Artista_se_pueda_ingresar_como_minimo_1_caracter(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar campo Artista con un solo carácter"):
        test_logger.info("Ingresando un solo carácter en 'Artista'")
        
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_edit_mode()
        profile.editar_nombre("a")
        profile.guardar_cambios()
        test_logger.info("Guardado con mínimo 1 carácter")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC011 - No permitir guardar campo Artista vacío")
@allure.description("""
Description
El usuario borra el contenido del campo “Artista” e intenta guardar el perfil.

Resultado esperado : No se permite guardar y se muestra un mensaje de validación indicando que el campo es obligatorio. No se persisten cambios.

Pre-conditions
SO/Navegador: Windows/macOS/Linux con Chrome/Edge/Firefox
Aplicación web Audius accesible
Sesión iniciada válida
Perfil del usuario cargado
""")
@pytest.mark.functional
@pytest.mark.integration
def test_TC011_Verificar_que_no_permita_guardar_vacio_el_campo_de_artista(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar guardar campo Artista vacío"):
        test_logger.info("Probando guardar 'Artista' vacío")
        
        profile.open_profile()
        feed.handle_notification_modal()
        profile.open_edit_mode()
        profile.editar_nombre("")
        profile.guardar_cambios()
