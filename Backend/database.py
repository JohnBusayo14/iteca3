# # # database.py
# # from sqlalchemy import create_engine
# # from sqlalchemy.ext.declarative import declarative_base
# # from sqlalchemy.orm import sessionmaker

# # # PostgreSQL connection URL
# # # Format: postgresql://username:password@host:port/database_name
# # # Replace with your PostgreSQL credentials
# # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:animashaun@localhost:5432/weba"

# # # Create the SQLAlchemy engine
# # engine = create_engine(SQLALCHEMY_DATABASE_URL)

# # # Create a session factory
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # # Base class for SQLAlchemy models
# # Base = declarative_base()

# # # Dependency to get the database session
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #         print("John")
# #     finally:
# #         db.close()


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL = "postgresql://postgres:animashaun@localhost:5432/weba"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:animashaun@localhost:5432/weba"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



