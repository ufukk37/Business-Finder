"""
BizFinder - İşletme Keşif Platformu
Ana FastAPI uygulaması
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.api import search, businesses, exports, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Uygulama başlangıç ve kapanış işlemleri"""
    # Veritabanı tablolarını oluştur
    Base.metadata.create_all(bind=engine)
    print("✅ Veritabanı tabloları oluşturuldu")
    yield
    print("👋 Uygulama kapatılıyor...")


app = FastAPI(
    title="BizFinder API",
    description="İşletme keşif ve yönetim platformu API'si",
    version="2.0.0",
    lifespan=lifespan
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router, prefix="/api/auth", tags=["Kimlik Doğrulama"])
app.include_router(search.router, prefix="/api/search", tags=["Arama"])
app.include_router(businesses.router, prefix="/api/businesses", tags=["İşletmeler"])
app.include_router(exports.router, prefix="/api/exports", tags=["Dışa Aktarım"])


@app.get("/")
async def root():
    return {
        "name": "BizFinder API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
