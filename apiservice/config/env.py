from typing import Final
from dotenv import load_dotenv
import os


load_dotenv()

SECRET: Final = os.getenv("SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

DB_NAME = os.getenv("NAME")
DB_LOGIN = os.getenv("LOGIN")
DB_PASS = os.getenv("PASS")
DB_PORT = os.getenv("PORT")
DB_HOST = os.getenv("HOST")

R_HOST = os.getenv("R_HOST")
R_PASS = os.getenv("R_PASS")

if not R_PASS:
    R_PASS = None

R_PORT = os.getenv("R_PORT")


ADMIN = os.getenv("ADMIN")
