import pytest
import re
from pages.login_page import LoginPage
from config.settings import settings
from playwright.sync_api import expect

@pytest.mark.login
def test_login_exitoso(page):
    login = LoginPage(page)
    login.open()
    login.login(settings.user_email, settings.user_password)

    if page.locator(login.MFA_INPUT).is_visible():
        print("\n🔐 Ingresa el código de verificación y presiona ENTER en la app.")
        page.wait_for_selector(login.MFA_INPUT, timeout=90000)
        login.wait_mfa_and_pause()  # aquí pausas y colocas el código
    page.wait_for_url(re.compile(r".*/feed.*"), timeout=40000)
    expect(page).to_have_url(re.compile(r".*/feed.*"), timeout=5000)
    print(f"✅ Inicio de sesión completado. URL actual: {page.url}")

@pytest.mark.login
def test_login_invalido_muestra_error(page):
    login = LoginPage(page)
    login.open()
    login.login("correo_invalido@example.com", "ClaveIncorrecta!")
    login.assert_login_error()
