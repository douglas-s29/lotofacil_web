"""
Generator API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services import CombinationGeneratorService
from app.schemas import GeneratorRequest, GeneratorResponse

router = APIRouter()


@router.post("/generate", response_model=GeneratorResponse)
async def generate_combinations(
    request: GeneratorRequest,
    db: Session = Depends(get_db)
):
    """Generate lottery combinations"""
    try:
        result = CombinationGeneratorService.generate_combinations(
            db=db,
            lottery_type=request.lottery_type,
            numbers_count=request.numbers_count,
            games_count=request.games_count,
            fixed_numbers=request.fixed_numbers,
            include_frequent=request.include_frequent,
            include_delayed=request.include_delayed,
            mix_strategy=request.mix_strategy
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/validate")
async def validate_combination(
    lottery_type: str,
    numbers: List[int],
    db: Session = Depends(get_db)
):
    """Validate a combination"""
    try:
        result = CombinationGeneratorService.validate_combination(
            db=db,
            lottery_type=lottery_type,
            numbers=numbers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
