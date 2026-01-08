"""
Lotteries API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import LotteryConfiguration, Draw
from app.schemas import LotteryConfig
from typing import List
from sqlalchemy import desc

router = APIRouter()


@router.get("/", response_model=List[LotteryConfig])
async def list_lotteries(db: Session = Depends(get_db)):
    """List all lottery configurations"""
    lotteries = db.query(LotteryConfiguration).all()
    return lotteries


@router.get("/{lottery_type}", response_model=LotteryConfig)
async def get_lottery(lottery_type: str, db: Session = Depends(get_db)):
    """Get specific lottery configuration"""
    lottery = db.query(LotteryConfiguration).filter(
        LotteryConfiguration.lottery_type == lottery_type
    ).first()
    
    if not lottery:
        raise HTTPException(status_code=404, detail="Lottery not found")
    
    return lottery


@router.get("/{lottery_type}/draws")
async def list_draws(
    lottery_type: str,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List draws for a lottery"""
    draws = db.query(Draw).filter(
        Draw.lottery_type == lottery_type
    ).order_by(desc(Draw.contest_number)).offset(offset).limit(limit).all()
    
    return draws


@router.get("/{lottery_type}/draws/latest")
async def get_latest_draw(lottery_type: str, db: Session = Depends(get_db)):
    """Get latest draw for a lottery"""
    draw = db.query(Draw).filter(
        Draw.lottery_type == lottery_type
    ).order_by(desc(Draw.contest_number)).first()
    
    if not draw:
        raise HTTPException(status_code=404, detail="No draws found")
    
    return draw


@router.get("/{lottery_type}/draws/{contest_number}")
async def get_draw(
    lottery_type: str,
    contest_number: int,
    db: Session = Depends(get_db)
):
    """Get specific draw by contest number"""
    draw = db.query(Draw).filter(
        Draw.lottery_type == lottery_type,
        Draw.contest_number == contest_number
    ).first()
    
    if not draw:
        raise HTTPException(status_code=404, detail="Draw not found")
    
    return draw
