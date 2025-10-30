import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()  # carga variables desde .env

@pytest.fixture(scope="session", autouse=True)
def storage_state():
    """Inicia sesión en Audius una vez y guarda el estado."""
    storage_path = "storageState.json"

    if os.path.exists(storage_path):
        print("✅ Reutilizando sesión existente.")
        return storage_path

    print("🔑 Iniciando sesión por primera vez...")

    with sync_playwright() as p:
        # 🔽 Esta parte es donde añadimos la variable HEADLESS
        headless = os.getenv("HEADLESS", "false").lower() == "true"
        browser = p.chromium.launch(headless=headless, slow_mo=200)
        page = browser.new_page()

        page.goto("https://audius.co/signin")
        page.get_by_label("Email").fill(os.getenv("AUDIUS_EMAIL"))
        page.locator('input[name="password"]').fill(os.getenv("AUDIUS_PASSWORD"))
        page.get_by_role("button", name="Sign In").click()
        page.wait_for_url("**/feed*", timeout=30000)
        print("🎵 Sesión iniciada correctamente.")

        page.context.storage_state(path=storage_path)
        browser.close()

    return storage_path


@pytest.fixture(scope="function")
def page_with_session(storage_state):
    """Crea un nuevo navegador con la sesión guardada."""
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()
        yield page
        browser.close()
