# config.py
from pathlib import Path
from dotenv import load_dotenv
import os

# load .env from project root (or use find_dotenv)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)  # loads variables into os.environ

# helper getters (with types & defaults)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

print(f"Database Config - Host: {DB_HOST}, User: {DB_USER}, Name: {DB_NAME}")