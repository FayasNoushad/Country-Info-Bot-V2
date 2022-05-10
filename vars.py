import os
from dotenv import load_dotenv


load_dotenv()


SESSION_NAME = os.environ.get("SESSION_NAME", "Country-Info-Bot")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_OWNER = int(os.environ.get("BOT_OWNER"))
DATABASE_URL = os.environ.get("DATABASE_URL")
