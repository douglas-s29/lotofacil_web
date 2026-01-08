"""
Endpoints da API de Conferidor
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import ResultCheckerService
from app.schemas import CheckerRequest, CheckerResponse

router = APIRouter()


@router.post("/check", response_model=CheckerResponse)
async def check_combination(
    request: CheckerRequest,
    db: Session = Depends(get_db)
):
    """Conferir combinação contra resultados de sorteios"""
    try:
        result = ResultCheckerService.check_combination(
            db=db,
            lottery_type=request.lottery_type,
            numbers=request.numbers,
            contest_number=request.contest_number
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
