from config.settings import settings
from pages.base_page import BasePage
from playwright.sync_api import expect

class LoginPage(BasePage):

    EMAIL_INPUT = 'input[name="email"], [aria-label="Email"]'
    PASSWORD_INPUT = 'input[name="password"], [aria-label="Password"]'
    SUBMIT_BTN = 'button:has-text("Sign in"), button[type="submit"]'
    ERROR_ALERT = '[role="alert"], .error, .toast-error'
    MFA_INPUT = 'input[name="code"], input[autocomplete="one-time-code"]'

    def open(self):
        self.goto(f"{settings.base_url}{settings.login_path}")

    def login(self, email: str, password: str):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.SUBMIT_BTN)

    def assert_logged_in(self):
        """Verifica si el usuario fue redirigido correctamente al feed."""
        expect(self.page).to_have_url("https://audius.co/signin/confirm-email", timeout=15000)

    def assert_login_error(self):
        """Verifica que se mantenga en la página de login (sin redirigir)."""
        expect(self.page).to_have_url("https://audius.co/signin", timeout=10000)
        # opcional: también valida el mensaje de error
        if self.page.locator(self.ERROR_ALERT).count() > 0:
            expect(self.page.locator(self.ERROR_ALERT).first).to_be_visible()

    def wait_mfa_and_pause(self, timeout_ms=90000):
        """Detiene la ejecución para ingresar el código MFA manualmente."""
        if self.page.locator(self.MFA_INPUT).is_visible():
            self.page.wait_for_selector(self.MFA_INPUT, timeout=timeout_ms)
            self.page.pause()  # pausa para que escribas el código y confirmes
