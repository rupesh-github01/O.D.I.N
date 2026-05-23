# backend/app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://odin:odinpassword@localhost:5432/odin_db")

# Engine is the core interface to the database
engine = create_engine(DATABASE_URL)

# Session factory, each session is a conversation with the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()