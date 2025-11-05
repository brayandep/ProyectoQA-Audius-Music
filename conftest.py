# tests/conftest.py
import os
import pathlib
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, expect

# Config del proyecto
from config.settings import SIGNIN_URL, FEED_URL

# ──────────────────────────────────────────────────────────────────────────────
# Carga .env
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
if not USER_EMAIL or not USER_PASSWORD:
    raise RuntimeError("Faltan USER_EMAIL o USER_PASSWORD en .env")

# Ajustes ejecutables por ENV (con defaults razonables)
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"  # por defecto visible
SLOWMO = int(os.getenv("PW_SLOWMO", "150"))
UA = os.getenv(
    "PW_USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/118.0.5993.90 Safari/537.36",
)
VIEWPORT = {"width": int(os.getenv("PW_VW", "1280")), "height": int(os.getenv("PW_VH", "800"))}

ARTIFACTS_DIR = pathlib.Path("test-results")
VIDEOS_DIR = ARTIFACTS_DIR / "videos"
TRACES_DIR = ARTIFACTS_DIR / "traces"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
for d in (VIDEOS_DIR, TRACES_DIR, SCREENSHOTS_DIR):
    d.mkdir(parents=True, exist_ok=True)

STORAGE_PATH = pathlib.Path("storageState.json")


# ──────────────────────────────────────────────────────────────────────────────
# Hook para conocer el resultado del test en fixtures (éxito/falla)
# ──────────────────────────────────────────────────────────────────────────────
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ──────────────────────────────────────────────────────────────────────────────
# 1) Login una vez por sesión y guardar storageState.json
# ──────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session", autouse=True)
def storage_state(playwright: Playwright):
    """
    Inicia sesión en Audius una sola vez por sesión de Pytest y guarda storageState.json.
    Si ya existe, lo reutiliza.
    """
    if STORAGE_PATH.exists():
        print("✅ Reutilizando sesión existente (storageState.json).")
        return str(STORAGE_PATH)

    print("🔑 Iniciando sesión por primera vez…")
    browser = playwright.chromium.launch(headless=False, slow_mo=SLOWMO)  # visible para evitar bloqueos
    context = browser.new_context(user_agent=UA, viewport=VIEWPORT, record_video_dir=str(VIDEOS_DIR))
    page = context.new_page()

    # Abre login
    page.goto(SIGNIN_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)  # pequeña pausa humana

    # Completa credenciales
    page.get_by_label("Email").fill(USER_EMAIL)
    page.locator('input[name="password"]').fill(USER_PASSWORD)
    page.wait_for_timeout(800)
    page.get_by_role("button", name="Sign In").click()

    # Espera al feed
    try:
        page.wait_for_url(f"{FEED_URL}*", timeout=60_000)
        print("🎵 Sesión iniciada correctamente.")
    except Exception:
        page.screenshot(path=str(ARTIFACTS_DIR / "login_error.png"), full_page=True)
        context.close()
        browser.close()
        raise RuntimeError("❌ No se pudo iniciar sesión. Revisa test-results/login_error.png")

    # Guarda el estado y cierra
    context.storage_state(path=str(STORAGE_PATH))
    context.close()
    browser.close()
    return str(STORAGE_PATH)


# ──────────────────────────────────────────────────────────────────────────────
# 2) Contexto por test usando la sesión guardada + tracing
# ──────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def context(playwright: Playwright, storage_state, request):
    """
    Crea un contexto por test con la sesión guardada.
    Arranca tracing y lo guarda si el test falla.
    """
    browser = playwright.chromium.launch(headless=HEADLESS, slow_mo=SLOWMO)
    context = browser.new_context(
        storage_state=storage_state,
        user_agent=UA,
        viewport=VIEWPORT,
        record_video_dir=str(VIDEOS_DIR),
    )
    # Tracing por test
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Guardar trace solo si falló
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        context.tracing.stop(path=str(trace_path))
        print(f"🧶 Trace guardado: {trace_path}")
    else:
        context.tracing.stop()  # sin path => no guarda archivo

    context.close()
    browser.close()


# ──────────────────────────────────────────────────────────────────────────────
# 3) Página por test 
# ──────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="function")
def page_with_session(context, request):
    """
    Devuelve una Page logueada y, si el test falla, captura screenshot.
    """
    page = context.new_page()
    yield page

    # Screenshot si falla
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        shot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        try:
            page.screenshot(path=str(shot_path), full_page=True)
            print(f"📸 Screenshot de falla: {shot_path}")
        except Exception:
            pass

    page.close()
