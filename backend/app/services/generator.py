"""
Combination generator service
Migrated from Django services
"""
from sqlalchemy.orm import Session
from app.models import LotteryConfiguration
from app.services.statistics import StatisticsService
from typing import List, Optional, Dict, Any
import random
import logging

logger = logging.getLogger(__name__)


class CombinationGeneratorService:
    """Service for generating lottery combinations"""
    
    @staticmethod
    def generate_combinations(
        db: Session,
        lottery_type: str,
        numbers_count: int,
        games_count: int,
        fixed_numbers: Optional[List[int]] = None,
        include_frequent: bool = False,
        include_delayed: bool = False,
        mix_strategy: bool = True
    ) -> Dict[str, Any]:
        """Generate lottery combinations based on filters"""
        logger.info(f"Generating {games_count} combinations for {lottery_type}")
        
        # Get lottery configuration
        config = db.query(LotteryConfiguration).filter(
            LotteryConfiguration.lottery_type == lottery_type
        ).first()
        
        if not config:
            raise ValueError(f"Configuration not found for {lottery_type}")
        
        # Validate numbers_count
        if numbers_count < (config.min_bet_numbers or config.numbers_to_pick):
            raise ValueError(f"Minimum numbers: {config.min_bet_numbers or config.numbers_to_pick}")
        if numbers_count > (config.max_bet_numbers or config.numbers_to_pick):
            raise ValueError(f"Maximum numbers: {config.max_bet_numbers or config.numbers_to_pick}")
        
        # Build number pool
        pool = set()
        
        if include_frequent:
            frequent = StatisticsService.get_most_frequent(db, lottery_type, limit=20)
            pool.update([stat.number for stat in frequent])
        
        if include_delayed:
            delayed = StatisticsService.get_most_delayed(db, lottery_type, limit=20)
            pool.update([stat.number for stat in delayed])
        
        if mix_strategy or not pool:
            # Add random numbers from the full range
            all_numbers = list(range(1, config.total_numbers + 1))
            pool.update(all_numbers)
        
        pool = list(pool)
        
        # Generate combinations
        combinations = []
        fixed_numbers = fixed_numbers or []
        
        for _ in range(games_count):
            combination = set(fixed_numbers)
            remaining = numbers_count - len(combination)
            
            # Filter pool to exclude fixed numbers
            available = [n for n in pool if n not in combination]
            
            # Randomly select remaining numbers
            if remaining > 0 and available:
                selected = random.sample(available, min(remaining, len(available)))
                combination.update(selected)
            
            combinations.append(sorted(list(combination)))
        
        return {
            "lottery_type": lottery_type,
            "combinations": combinations,
            "metadata": {
                "numbers_per_game": numbers_count,
                "total_games": len(combinations),
                "fixed_numbers": fixed_numbers,
                "include_frequent": include_frequent,
                "include_delayed": include_delayed,
            }
        }
    
    @staticmethod
    def validate_combination(
        db: Session,
        lottery_type: str,
        numbers: List[int]
    ) -> Dict[str, Any]:
        """Validate a combination"""
        config = db.query(LotteryConfiguration).filter(
            LotteryConfiguration.lottery_type == lottery_type
        ).first()
        
        if not config:
            return {
                "valid": False,
                "errors": [f"Configuration not found for {lottery_type}"],
                "warnings": []
            }
        
        errors = []
        warnings = []
        
        # Check number count
        if len(numbers) < (config.min_bet_numbers or config.numbers_to_pick):
            errors.append(f"Minimum {config.min_bet_numbers or config.numbers_to_pick} numbers required")
        
        if len(numbers) > (config.max_bet_numbers or config.numbers_to_pick):
            errors.append(f"Maximum {config.max_bet_numbers or config.numbers_to_pick} numbers allowed")
        
        # Check number range
        for num in numbers:
            if num < 1 or num > config.total_numbers:
                errors.append(f"Number {num} is out of range (1-{config.total_numbers})")
        
        # Check for duplicates
        if len(numbers) != len(set(numbers)):
            errors.append("Duplicate numbers found")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
