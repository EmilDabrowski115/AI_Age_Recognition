from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sqlite3
from ..config import DATABASE_URL



# SQLite engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initalize_database():
    # Extract SQLite file path from DATABASE_URL
    if DATABASE_URL.startswith("sqlite:///"):
        db_file = DATABASE_URL.replace("sqlite:///", "")
    else:
        raise ValueError("Only SQLite is supported for init_database")

    if not os.path.exists(db_file):
        print(f"Database file '{db_file}' not found. Creating...")
        # Read schema.sql and execute
        with open("backend/database/schema.sql", "r") as f:
            schema_sql = f.read()

        conn = sqlite3.connect(db_file)
        try:
            cursor = conn.cursor()
            cursor.executescript(schema_sql)
            conn.commit()
        finally:
            conn.close()

        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
        print(f"Database '{db_file}' created successfully.")
    else:
        print(f"Database '{db_file}' already exists. Skipping creation.")
