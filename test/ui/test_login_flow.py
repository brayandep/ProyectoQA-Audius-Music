import pytest
from pages.login_page import LoginPage
from config.settings import settings

@pytest.mark.login
def test_login_exitoso(page):
    login = LoginPage(page)
    login.open()
    login.login(settings.user_email, settings.user_password)
    
    # Espera manual para MFA (solo si aparece)
    if page.locator(login.MFA_INPUT).is_visible():
        login.wait_mfa_and_pause()
    timeout=15000
    login.assert_logged_in()

@pytest.mark.login
def test_login_invalido_muestra_error(page):
    login = LoginPage(page)
    login.open()
    login.login("correo_invalido@example.com", "ClaveIncorrecta!")
    login.assert_login_error()
