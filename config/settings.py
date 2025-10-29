from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://audius.co")
    login_path: str = os.getenv("LOGIN_PATH", "/login")
    user_email: str = os.getenv("USER_EMAIL", "")
    user_password: str = os.getenv("USER_PASSWORD", "")
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    browser: str = os.getenv("BROWSER", "chromium")
    viewport_width: int = int(os.getenv("VIEWPORT_WIDTH", "1366"))
    viewport_height: int = int(os.getenv("VIEWPORT_HEIGHT", "768"))

settings = Settings()
