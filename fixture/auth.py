from pages.login_page import LoginPage
from config.settings import settings

def do_login(page):
    lp = LoginPage(page)
    lp.open()
    lp.login(settings.user_email, settings.user_password)
    lp.assert_logged_in()
