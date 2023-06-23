from os import getenv
from dotenv import load_dotenv

load_dotenv()

# BOT CONNECTION PARAM

API_ID, API_HASH = int(getenv("api_id")), getenv("api_hash")

# DATABASE CONNECTION PARAM

DB_HOST = getenv("DATABASE_HOST")
DB_PORT = getenv("DATABASE_PORT")
DB_LOGIN = getenv("DATABASE_LOGIN")
DB_PASS = getenv("DATABASE_PASS")
DB_NAME = getenv("DATABASE_NAME")

# REDIS CONNECTION PARAM

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT"))

# CONTACTS EMAIL

ADMIN = getenv("ADMIN_EMAIL")
ADMIN2 = getenv("ADMIN_EMAIL2")
