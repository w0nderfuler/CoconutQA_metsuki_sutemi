import os
from dotenv import load_dotenv

load_dotenv()

class PostgresCreds:
    USERNAME = os.getenv("DATABASE_USERNAME")
    PASSWORD = os.getenv("DATABASE_PASSWORD")
    HOST = os.getenv("DATABASE_HOST")
    PORT = os.getenv("DATABASE_PORT")
    NAME = os.getenv("DATABASE_NAME")