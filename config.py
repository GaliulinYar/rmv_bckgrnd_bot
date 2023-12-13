from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

TOKEN = os.getenv('MY_TOKEN')
BASE_SQLITE = os.getenv('BASE_SQLITE_PATH')
ID_ADMIN = os.getenv('ID_ADMIN')
