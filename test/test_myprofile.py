# test/test_myprofile.py
import pytest
from pages.yourfeed_page import YourFeedPage
from pages.myprofile_page import MyProfilePage

# ===========================================================
# TEST FUNCIONALES DEL MÓDULO "MY PROFILE" (Audius Music)
# Flujo: Your Feed → clic en avatar → Perfil → acciones
# ===========================================================

@pytest.mark.functional
def test_TC001_abrir_modal_followers(page_with_session):
    """Verifica que al hacer clic en 'Followers' se abra el modal correspondiente."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    feed.go_to_my_profile()

    profile.open_followers_modal()


@pytest.mark.functional
def test_TC002_abrir_modal_following(page_with_session):
    """Verifica que al hacer clic en 'Following' se abra el modal correspondiente."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    feed.go_to_my_profile()

    profile.open_following_modal()


@pytest.mark.functional
def test_TC003_abrir_modal_share_profile(page_with_session):
    """Verifica que al hacer clic en 'Share' se abra el modal de compartir perfil."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    feed.go_to_my_profile()

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
    feed.go_to_my_profile()

    profile.try_empty_song_name()


@pytest.mark.negative
def test_TC005_no_guardar_nombre_con_espacios(page_with_session):
    """Verifica que no se pueda editar el nombre de una canción con solo espacios."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    feed.go_to_my_profile()

    profile.try_blank_song_name()


@pytest.mark.negative
def test_TC006_no_guardar_foto_perfil_vacia(page_with_session):
    """Verifica que no se guarde la foto de perfil si no se ha cargado ninguna."""
    feed = YourFeedPage(page_with_session)
    profile = MyProfilePage(page_with_session)

    feed.open()
    feed.handle_notification_modal()
    feed.go_to_my_profile()

    profile.try_save_empty_profile_picture()
