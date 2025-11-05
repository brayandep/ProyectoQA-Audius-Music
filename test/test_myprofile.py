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
@allure.title("TC001 - Abrir modal de Followers")
@pytest.mark.functional
def test_TC001_abrir_modal_followers(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Abrir módulo Your Feed"):
        test_logger.info("Navegando a Your Feed")
        feed.open()
        feed.handle_notification_modal()

    with allure.step("Abrir el perfil del usuario"):
        test_logger.info("Abriendo perfil del usuario desde el avatar")
        profile.open_profile()

    with allure.step("Abrir el modal de Followers"):
        test_logger.info("Abriendo modal 'Followers'")
        profile.open_followers_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC002 - Abrir modal de Following")
@pytest.mark.functional
def test_TC002_abrir_modal_following(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Navegar al perfil"):
        test_logger.info("Entrando a Your Feed y cerrando modales iniciales")
        feed.open()
        feed.handle_notification_modal()
        test_logger.info("Abriendo perfil")
        profile.open_profile()

    with allure.step("Abrir modal Following"):
        test_logger.info("Abriendo modal 'Following'")
        profile.open_following_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC003 - Abrir modal de compartir perfil")
@pytest.mark.functional
def test_TC003_abrir_modal_share_profile(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Abrir perfil y compartir"):
        test_logger.info("Abriendo Your Feed → Perfil → Share")
        feed.open()
        feed.handle_notification_modal()
        profile.open_profile()
        profile.open_share_modal()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC004 - No guardar nombre vacío en track")
@pytest.mark.functional
def test_TC004_no_guardar_nombre_vacio(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar editar un track con nombre vacío"):
        test_logger.info("Abriendo edición de track y probando nombre vacío")
        feed.open()
        feed.handle_notification_modal()
        profile.open_profile()
        profile.open_track_for_edit()
        profile.try_empty_song_name()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC005 - No guardar nombre con solo espacios")
@pytest.mark.functional
@pytest.mark.xfail(reason="Permite espacios en blanco en campo Name de track")
def test_TC005_no_guardar_nombre_con_espacios(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar guardar con nombre de solo espacios"):
        test_logger.info("Probando nombre con solo espacios")
        feed.open()
        feed.handle_notification_modal()
        profile.open_profile()
        profile.open_track_for_edit()
        profile.try_blank_song_name()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TC006 - No guardar imagen vacía en track")
@pytest.mark.functional
def test_TC006_guardar_foto_perfil_de_track_vacia(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Verificar guardar sin imagen de perfil"):
        test_logger.info("Intentando guardar track sin seleccionar imagen")
        feed.open()
        feed.handle_notification_modal()
        profile.open_profile()
        profile.open_track_for_edit()
        profile.try_save_empty_profile_picture()


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC007 - Editar descripción con caracteres válidos")
@pytest.mark.functional
def test_TC007_editar_descripcion_con_caracteres_validos(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar descripción con texto válido"):
        test_logger.info("Editando descripción del perfil")
        feed.open()
        profile.open_profile()
        profile.open_edit_mode()
        profile.editar_descripcion("Perfil actualizado automáticamente desde Playwright QA 🧠")
        profile.guardar_cambios()
        test_logger.info("Descripción guardada correctamente")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC008 - Editar nombre del artista con datos válidos")
@pytest.mark.functional
def test_TC008_editar_el_campo_Nombre_artista_con_datos_validos(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar campo Artista con nombre válido"):
        test_logger.info("Editando nombre de artista → 'QA Tester Automation'")
        feed.open()
        profile.open_profile()
        profile.open_edit_mode()
        profile.editar_nombre("QA Tester Automation")
        profile.guardar_cambios()
        test_logger.info("Nombre de artista guardado")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC009 - No superar 30 caracteres en campo Artista")
@pytest.mark.functional
@pytest.mark.xfail(reason="No se muestra mensaje al superar los 30 caracteres; el sistema solo corta el texto")
def test_TC009_Verificar_que_al_editar_el_campo_Artista_no_Supere_los_30_caracteres_mostrando_un_mensaje(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar ingresar más de 30 caracteres"):
        test_logger.info("Probando validación de longitud >30 en 'Artista'")
        feed.open()
        profile.open_profile()
        profile.open_edit_mode()
        profile.editar_nombre("LaamistadesunarelaciónafectivaentredosomáspersonasLaamistadesunarelaciónafectivaentredosomáspersonas")
        profile.guardar_cambios()

    with allure.step("Validar mensaje de error mostrado"):
        test_logger.info("Verificando mensaje 'Fix errors to continue.'")
        assert profile.validar_mensaje("Fix errors to continue."), "❌ No se mostró el mensaje esperado"


@allure.feature("My Profile")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("TC010 - Permitir mínimo 1 caracter en campo Artista")
@pytest.mark.functional
def test_TC010_Verificar_que_al_editar_el_campo_Artista_se_pueda_ingresar_como_minimo_1_caracter(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Editar campo Artista con un solo carácter"):
        test_logger.info("Ingresando un solo carácter en 'Artista'")
        feed.open()
        profile.open_profile()
        profile.open_edit_mode()
        profile.editar_nombre("a")
        profile.guardar_cambios()
        test_logger.info("Guardado con mínimo 1 carácter")


@allure.feature("My Profile")
@allure.severity(allure.severity_level.MINOR)
@allure.title("TC011 - No permitir guardar campo Artista vacío")
@pytest.mark.functional
def test_TC011_Verificar_que_no_permita_guardar_vacio_el_campo_de_artista(page_with_session, test_logger):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    with allure.step("Intentar guardar campo Artista vacío"):
        test_logger.info("Probando guardar 'Artista' vacío")
        feed.open()
        profile.open_profile()
        profile.open_edit_mode()
        profile.editar_nombre("")
        profile.guardar_cambios()
