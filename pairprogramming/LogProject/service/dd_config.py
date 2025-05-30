import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
class db_config():
    load_dotenv()
    # print(f"DB_USER: {os.getenv("DB_USER)}")
    # print(f"DB_PASS: {DB_PASS}")
    # print(f"DB_HOST: {DB_HOST}")
    # print(f"DB_PORT: {DB_PORT}")
    # print(f"DB_NAME: {DB_NAME}")
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_PASS = os.getenv("DB_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_PASS = quote_plus(DB_PASS)
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL, echo=True)
    session= sessionmaker(autocommit=False, autoflush=False, bind=engine)
