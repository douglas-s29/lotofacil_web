"""
Serviço de conferidor de resultados
Migrado dos serviços Django
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import Draw
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ResultCheckerService:
    """Serviço para conferir combinações contra resultados de sorteios"""
    
    @staticmethod
    def check_combination(
        db: Session,
        lottery_type: str,
        numbers: List[int],
        contest_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """Conferir combinação contra um sorteio específico ou o último sorteio"""
        logger.info(f"Conferindo combinação para {lottery_type}")
        
        # Get the draw
        if contest_number:
            draw = db.query(Draw).filter(
                Draw.lottery_type == lottery_type,
                Draw.contest_number == contest_number
            ).first()
        else:
            draw = db.query(Draw).filter(
                Draw.lottery_type == lottery_type
            ).order_by(desc(Draw.contest_number)).first()
        
        if not draw:
            return {
                "found": False,
                "contest_number": None,
                "draw_date": None,
                "drawn_numbers": None,
                "user_numbers": numbers,
                "matches": [],
                "match_count": 0,
                "is_winner": False
            }
        
        # Calculate matches
        drawn_numbers = draw.numbers
        matches = [num for num in numbers if num in drawn_numbers]
        match_count = len(matches)
        
        # Determine if winner (this depends on lottery rules)
        # For Lotofácil: 11+ matches wins
        # For Mega-Sena: 4+ matches wins (quadra), 5+ (quina), 6 (sena)
        is_winner = False
        if lottery_type == "LOTOFACIL":
            is_winner = match_count >= 11
        elif lottery_type == "MEGA_SENA":
            is_winner = match_count >= 4
        elif lottery_type == "QUINA":
            is_winner = match_count >= 2
        
        return {
            "found": True,
            "contest_number": draw.contest_number,
            "draw_date": draw.draw_date,
            "drawn_numbers": sorted(drawn_numbers),
            "user_numbers": sorted(numbers),
            "matches": sorted(matches),
            "match_count": match_count,
            "is_winner": is_winner
        }
