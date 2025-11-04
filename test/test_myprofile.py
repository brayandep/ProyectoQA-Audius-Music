# test/test_myprofile.py
import pytest
from pages.yourfeed_page import YourFeedPage
from pages.myprofile_page import MyProfilePage

# ===========================================================
# TEST FUNCIONALES DEL MÓDULO "MY PROFILE" (Audius Music)
# Flujo: Your Feed → clic en avatar → Perfil → acciones
# ===========================================================

@pytest.mark.run
def test_TC001_abrir_modal_followers(page_with_session):
    """Verifica que al hacer clic en 'Followers' se abra el modal correspondiente."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.open_followers_modal()


@pytest.mark.functional
def test_TC002_abrir_modal_following(page_with_session):
    """Verifica que al hacer clic en 'Following' se abra el modal correspondiente."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.open_following_modal()


@pytest.mark.functional
def test_TC003_abrir_modal_share_profile(page_with_session):
    """Verifica que al hacer clic en 'Share' se abra el modal de compartir perfil."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.open_share_modal()


# ===========================================================
# TEST NEGATIVOS (validaciones de edición / perfil)
# ===========================================================

@pytest.mark.negative
def test_TC004_no_guardar_nombre_vacio(page_with_session):
    """Verifica que no se pueda editar el nombre de una canción vacío."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.try_empty_song_name()


@pytest.mark.negative
def test_TC005_no_guardar_nombre_con_espacios(page_with_session):
    """Verifica que no se pueda editar el nombre de una canción con solo espacios."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.try_blank_song_name()


@pytest.mark.negative
def test_TC006_no_guardar_foto_perfil_vacia(page_with_session):
    """Verifica que no se guarde la foto de perfil si no se ha cargado ninguna."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    profile.open_profile()

    profile.try_save_empty_profile_picture()


@pytest.mark.functional
def test_TC007_editar_descripcion_con_caracteres_validos(page_with_session):
    
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_descripcion("Perfil actualizado automáticamente desde Playwright QA 🧠")
    profile.guardar_cambios()

@pytest.mark.functional
def test_TC008_editar_el_campo_Nombre_artista_con_datos_validos(page_with_session):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_nombre("QA Tester Automation")
    profile.guardar_cambios()

@pytest.mark.xfail(reason="Nose muestra ningun mensaje de validacion al superar los 30 caracteres, simplemente los corta")
@pytest.mark.functional
def test_TC009_Verificar_que_al_editar_el_campo_Artista_no_Supere_los_30_caracteres_mostrando_un_mensaje(page_with_session):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_nombre("LaamistadesunarelaciónafectivaentredosomáspersonasLaamistadesunarelaciónafectivaentredosomáspersonas")
    profile.guardar_cambios()
    assert profile.validar_mensaje("Fix errors to continue."), "❌ No se mostró el mensaje esperado"

@pytest.mark.functional
def test_TC010_Verificar_que_al_editar_el_campo_Artista_se_pueda_ingresar_como_minimo_1_caracter(page_with_session):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_nombre("a")
    profile.guardar_cambios()

@pytest.mark.xfail(reason="permite espacios en blanco en campo Name de artista")
@pytest.mark.functional
def test_TC010_Verificar_que_no_permita_ingresar_datos_vacios_en_el_campo_Artista(page_with_session):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_nombre(" ")
    profile.guardar_cambios()


@pytest.mark.functional
def test_TC011_Verificar_que_no_permita_guardar_vacio_el_campo_de_artista(page_with_session):
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)
    feed.open()
    profile.open_profile()
    profile.open_edit_mode()
    profile.editar_nombre("")
    profile.guardar_cambios()
