import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("LIBRARY_DB_HOST")
DB_USER = os.getenv("LIBRARY_DB_USER")
DB_PASSWORD = os.getenv("LIBRARY_DB_PASSWORD")
DB_NAME = os.getenv("LIBRARY_DB_NAME")