"""
FastAPI main application for Lotofácil Web
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import lotteries, statistics, generator, checker, combinations

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API moderna para análise de loterias e geração de números",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(lotteries.router, prefix="/api/lotteries", tags=["lotteries"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["statistics"])
app.include_router(generator.router, prefix="/api/generator", tags=["generator"])
app.include_router(checker.router, prefix="/api/checker", tags=["checker"])
app.include_router(combinations.router, prefix="/api/combinations", tags=["combinations"])


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "Lotofácil Web API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde"""
    return {"status": "healthy"}
