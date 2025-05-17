from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# SQL Server configuration
SERVER = os.getenv("SQL_SERVER", r"DESKTOP-OLBMVT3\SQLEXPRESS")  # Using raw string for correct escape
DATABASE = os.getenv("SQL_DATABASE", "ecommerce_admin")

# Connection string for Windows Authentication
DATABASE_URL = f"mssql+pyodbc://{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()