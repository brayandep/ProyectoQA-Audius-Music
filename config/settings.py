import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://audius.co").rstrip("/")
username= os.getenv("AUDIUS_HANDLE")
MYPROFILE_URL=f"{BASE_URL}/{username}"
SIGNIN_URL = f"{BASE_URL}/signin"
FEED_URL   = f"{BASE_URL}/feed"
UPLOAD_URL = f"{BASE_URL}/upload"
