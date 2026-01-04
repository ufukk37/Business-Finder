"""
Veritabanı bağlantı yapılandırması - SQLite
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Veritabanı dosyası yolu
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'business_finder.db')}"

# Engine oluştur
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class
Base = declarative_base()


def get_db():
    """Veritabanı oturumu sağlayıcı"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
