"""Configuration lue depuis les variables d'environnement (fichier .env)."""
import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "pro")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "1521"))
DB_SERVICE = os.getenv("DB_SERVICE", "XE")

SERIAL_PORT = os.getenv("SERIAL_PORT", "COM6")
SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", "115200"))

WEB_HOST = os.getenv("WEB_HOST", "127.0.0.1")
WEB_PORT = int(os.getenv("WEB_PORT", "5000"))
