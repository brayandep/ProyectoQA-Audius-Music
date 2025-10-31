import os
import pathlib
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from config.settings import SIGNIN_URL, FEED_URL 

# 🔹 Carga las variables desde el archivo .env (correo, contraseña, headless, etc.)
load_dotenv()

@pytest.fixture(scope="session", autouse=True)
def storage_state():
    """Inicia sesión en Audius una vez y guarda el estado de sesión."""
    storage_path = "storageState.json"

    # ✅ Si ya existe el archivo, reutilizamos la sesión
    if os.path.exists(storage_path):
        print("✅ Reutilizando sesión existente.")
        return storage_path

    print("🔑 Iniciando sesión por primera vez...")

    with sync_playwright() as p:
        # Forzamos modo visible (Cloudflare bloquea los headless)
        browser = p.chromium.launch(headless=False, slow_mo=300)

        #  Creamos un contexto con un user-agent real y sin señales de automatización
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.5993.90 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()

        #  Abrimos la página de inicio de sesión
        page.goto(SIGNIN_URL)
        page.wait_for_timeout(2000)  # espera 2s para evitar detección por velocidad

        #  Llenamos las credenciales desde el archivo .env
        email = os.getenv("USER_EMAIL")
        password = os.getenv("USER_PASSWORD")

        if not email or not password:
            raise ValueError("⚠️ Las variables AUDIUS_EMAIL o AUDIUS_PASSWORD no están definidas en .env")

        page.get_by_label("Email").fill(email)
        page.locator('input[name="password"]').fill(password)
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Sign In").click()

        #  Esperamos hasta que redirija al feed (puede tardar)
        try:
            page.wait_for_url(f"{FEED_URL}*", timeout=60000)
            print("🎵 Sesión iniciada correctamente.")
        except Exception:
            page.screenshot(path="login_error.png", full_page=True)
            raise RuntimeError("❌ No se pudo iniciar sesión. Revisa login_error.png.")

        # 🔹 Guardamos la sesión en archivo
        context.storage_state(path=storage_path)
        browser.close()

    return storage_path


@pytest.fixture(scope="function")
def page_with_session(storage_state):
    """Crea un nuevo navegador con la sesión guardada."""
    with sync_playwright() as p:
        #  Ejecución visible hasta confirmar que no hay bloqueo (puedes poner True luego)
        browser = p.chromium.launch(headless=False, slow_mo=150)
        context = browser.new_context(
            storage_state=storage_state,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/118.0.5993.90 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800}
        )

        page = context.new_page()
        yield page
        browser.close()
