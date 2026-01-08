"""
Endpoints da API de Estatísticas
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import StatisticsService
from app.schemas import NumberStatistics
from typing import List

router = APIRouter()


@router.get("/{lottery_type}", response_model=List[NumberStatistics])
async def get_statistics(
    lottery_type: str,
    limit: int = None,
    db: Session = Depends(get_db)
):
    """Obter estatísticas de uma loteria"""
    stats = StatisticsService.get_statistics(db, lottery_type, limit)
    return stats


@router.get("/{lottery_type}/frequent", response_model=List[NumberStatistics])
async def get_most_frequent(
    lottery_type: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Obter números mais frequentes"""
    stats = StatisticsService.get_most_frequent(db, lottery_type, limit)
    return stats


@router.get("/{lottery_type}/delayed", response_model=List[NumberStatistics])
async def get_most_delayed(
    lottery_type: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Obter números mais atrasados"""
    stats = StatisticsService.get_most_delayed(db, lottery_type, limit)
    return stats


@router.post("/{lottery_type}/calculate")
async def calculate_statistics(lottery_type: str, db: Session = Depends(get_db)):
    """Recalcular estatísticas de uma loteria"""
    try:
        StatisticsService.calculate_statistics(db, lottery_type)
        return {"message": f"Estatísticas calculadas para {lottery_type}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
