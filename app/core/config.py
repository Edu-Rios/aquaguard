import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()