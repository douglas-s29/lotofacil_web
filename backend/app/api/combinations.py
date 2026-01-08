"""
Endpoints da API de Combinações de Usuário
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.models import UserCombination
from app.schemas import UserCombination as UserCombinationSchema, UserCombinationCreate
from typing import List

router = APIRouter()


@router.get("/", response_model=List[UserCombinationSchema])
async def list_combinations(
    lottery_type: str = None,
    session_key: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Listar combinações do usuário"""
    query = db.query(UserCombination)
    
    if lottery_type:
        query = query.filter(UserCombination.lottery_type == lottery_type)
    
    if session_key:
        query = query.filter(UserCombination.session_key == session_key)
    
    combinations = query.order_by(desc(UserCombination.created_at)).limit(limit).all()
    return combinations


@router.post("/", response_model=UserCombinationSchema)
async def create_combination(
    combination: UserCombinationCreate,
    db: Session = Depends(get_db)
):
    """Criar uma nova combinação de usuário"""
    db_combination = UserCombination(**combination.model_dump())
    db.add(db_combination)
    db.commit()
    db.refresh(db_combination)
    return db_combination


@router.get("/{combination_id}", response_model=UserCombinationSchema)
async def get_combination(combination_id: int, db: Session = Depends(get_db)):
    """Obter combinação específica"""
    combination = db.query(UserCombination).filter(
        UserCombination.id == combination_id
    ).first()
    
    if not combination:
        raise HTTPException(status_code=404, detail="Combinação não encontrada")
    
    return combination


@router.delete("/{combination_id}")
async def delete_combination(combination_id: int, db: Session = Depends(get_db)):
    """Excluir uma combinação"""
    combination = db.query(UserCombination).filter(
        UserCombination.id == combination_id
    ).first()
    
    if not combination:
        raise HTTPException(status_code=404, detail="Combinação não encontrada")
    
    db.delete(combination)
    db.commit()
    return {"message": "Combinação excluída com sucesso"}


@router.put("/{combination_id}/favorite")
async def toggle_favorite(combination_id: int, db: Session = Depends(get_db)):
    """Alternar status de favorito"""
    combination = db.query(UserCombination).filter(
        UserCombination.id == combination_id
    ).first()
    
    if not combination:
        raise HTTPException(status_code=404, detail="Combinação não encontrada")
    
    combination.is_favorite = not combination.is_favorite
    db.commit()
    db.refresh(combination)
    return combination
