from dotenv import load_dotenv
import os

load_dotenv()

YANDEX_API = os.getenv('YANDEX_API')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')