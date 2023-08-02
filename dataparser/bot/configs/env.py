from os import getenv
from dotenv import load_dotenv


load_dotenv()

# BOT CONNECTION PARAM

CLIENT_API_ID, CLIENT_API_HASH = int(getenv("api_id")), getenv("api_hash")
CLIENT2_API_ID, CLIENT2_API_HASH = int(getenv("api_id2")), getenv("api_hash2")
CLIENT3_API_ID, CLIENT3_API_HASH = int(getenv("api_id3")), getenv("api_hash3")

CLIENTS = {"client": (CLIENT_API_ID, CLIENT_API_HASH),
           "client2": (CLIENT2_API_ID, CLIENT2_API_HASH),
           "client3": (CLIENT3_API_ID, CLIENT3_API_HASH)}

# DATABASE CONNECTION PARAM

DB_HOST = getenv("DATABASE_HOST")
DB_PORT = getenv("DATABASE_PORT")
DB_LOGIN = getenv("DATABASE_LOGIN")
DB_PASS = getenv("DATABASE_PASS")
DB_NAME = getenv("DATABASE_NAME")

# REDIS CONNECTION PARAM

REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT"))
REDIS_PASS = getenv("REDIS_PASS")


# CONTACTS EMAIL

ADMIN = getenv("ADMIN_EMAIL")
ADMIN2 = getenv("ADMIN_EMAIL2")
