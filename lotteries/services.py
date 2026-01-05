"""
Service classes for lottery business logic.

Adapted from Android app specification to Django.
"""
import random
from typing import List, Dict, Set, Optional
from django.core.cache import cache
from django.db.models import Count, Max, Min, Avg
from .models import Draw, NumberStatistics, LotteryType, LotteryConfiguration


class StatisticsService:
    """Service for calculating and caching lottery statistics."""
    
    CACHE_TIMEOUT = 3600  # 1 hour
    
    @staticmethod
    def calculate_statistics(lottery_type: str) -> None:
        """
        Calculate and update statistics for all numbers in a lottery type.
        
        Args:
            lottery_type: Type of lottery (e.g., 'MEGA_SENA', 'LOTOFACIL')
        """
        draws = Draw.objects.filter(lottery_type=lottery_type).order_by('-contest_number')
        
        if not draws.exists():
            return
        
        config = LotteryConfiguration.objects.get(lottery_type=lottery_type)
        latest_contest = draws.first().contest_number
        
        # Calculate statistics for each number
        for number in range(1, config.total_numbers + 1):
            frequency = 0
            last_contest = None
            delays = []
            last_seen = None
            
            for draw in draws.reverse():  # Process chronologically
                numbers = draw.get_numbers_display()
                
                if number in numbers:
                    frequency += 1
                    if last_seen is not None:
                        delays.append(draw.contest_number - last_seen)
                    last_seen = draw.contest_number
                    last_contest = draw.contest_number
            
            # Calculate delay (contests since last appearance)
            delay = latest_contest - last_contest if last_contest else latest_contest
            
            # Calculate average and max delay
            avg_delay = sum(delays) / len(delays) if delays else 0
            max_delay = max(delays) if delays else delay
            
            # Update or create statistics
            NumberStatistics.objects.update_or_create(
                lottery_type=lottery_type,
                number=number,
                defaults={
                    'frequency': frequency,
                    'last_draw_contest': last_contest,
                    'delay': delay,
                    'max_delay': max_delay,
                    'average_delay': avg_delay,
                }
            )
        
        # Invalidate cache
        cache_key = f'stats_{lottery_type}'
        cache.delete(cache_key)
    
    @staticmethod
    def get_statistics(lottery_type: str, force_refresh: bool = False) -> List[NumberStatistics]:
        """
        Get statistics for a lottery type (cached).
        
        Args:
            lottery_type: Type of lottery
            force_refresh: Force recalculation of statistics
            
        Returns:
            List of NumberStatistics objects
        """
        cache_key = f'stats_{lottery_type}'
        
        if force_refresh:
            cache.delete(cache_key)
        
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = list(NumberStatistics.objects.filter(
                lottery_type=lottery_type
            ).order_by('number'))
            cache.set(cache_key, stats, StatisticsService.CACHE_TIMEOUT)
        
        return stats
    
    @staticmethod
    def get_most_frequent(lottery_type: str, limit: int = 10) -> List[NumberStatistics]:
        """Get most frequent numbers."""
        return NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('-frequency')[:limit]
    
    @staticmethod
    def get_most_delayed(lottery_type: str, limit: int = 10) -> List[NumberStatistics]:
        """Get most delayed numbers."""
        return NumberStatistics.objects.filter(
            lottery_type=lottery_type
        ).order_by('-delay')[:limit]


class CombinationGeneratorService:
    """Service for generating lottery combinations with filters."""
    
    @staticmethod
    def generate_combinations(
        lottery_type: str,
        numbers_count: int,
        games_count: int = 1,
        fixed_numbers: Optional[List[int]] = None,
        include_frequent: bool = True,
        include_delayed: bool = True,
        mix_strategy: bool = True
    ) -> List[List[int]]:
        """
        Generate lottery combinations based on filters.
        
        Args:
            lottery_type: Type of lottery
            numbers_count: How many numbers in each game
            games_count: How many games to generate
            fixed_numbers: Numbers that must appear in all combinations
            include_frequent: Include frequently drawn numbers
            include_delayed: Include delayed numbers
            mix_strategy: Mix different strategies
            
        Returns:
            List of combinations (each combination is a list of numbers)
        """
        config = LotteryConfiguration.objects.get(lottery_type=lottery_type)
        stats = StatisticsService.get_statistics(lottery_type)
        
        fixed_numbers = fixed_numbers or []
        games = []
        
        # Build number pools based on filters
        all_numbers = set(range(1, config.total_numbers + 1))
        
        if not include_frequent and not include_delayed:
            # Random selection from all numbers
            available_numbers = list(all_numbers)
        else:
            available_numbers = set()
            
            if include_frequent:
                frequent = StatisticsService.get_most_frequent(lottery_type, 20)
                available_numbers.update([s.number for s in frequent])
            
            if include_delayed:
                delayed = StatisticsService.get_most_delayed(lottery_type, 20)
                available_numbers.update([s.number for s in delayed])
            
            if mix_strategy and include_frequent and include_delayed:
                # Add some random numbers for mixing
                remaining = all_numbers - available_numbers
                if remaining:
                    random_picks = random.sample(
                        list(remaining),
                        min(10, len(remaining))
                    )
                    available_numbers.update(random_picks)
            
            available_numbers = list(available_numbers)
        
        # Generate combinations
        for _ in range(games_count):
            game = set(fixed_numbers)
            
            # Remove fixed numbers from available pool for this game
            temp_available = [n for n in available_numbers if n not in game]
            
            # Fill remaining slots
            remaining_count = numbers_count - len(game)
            if remaining_count > 0 and temp_available:
                selected = random.sample(
                    temp_available,
                    min(remaining_count, len(temp_available))
                )
                game.update(selected)
            
            # If we don't have enough numbers, fill with random from all numbers
            if len(game) < numbers_count:
                all_available = [n for n in all_numbers if n not in game]
                needed = numbers_count - len(game)
                if all_available:
                    selected = random.sample(
                        all_available,
                        min(needed, len(all_available))
                    )
                    game.update(selected)
            
            games.append(sorted(list(game)))
        
        return games
    
    @staticmethod
    def validate_combination(
        lottery_type: str,
        numbers: List[int]
    ) -> Dict[str, any]:
        """
        Validate a combination against lottery rules.
        
        Args:
            lottery_type: Type of lottery
            numbers: List of numbers to validate
            
        Returns:
            Dictionary with validation results
        """
        config = LotteryConfiguration.objects.get(lottery_type=lottery_type)
        
        errors = []
        warnings = []
        
        # Check count
        if len(numbers) < config.min_bet_numbers:
            errors.append(f'Mínimo de {config.min_bet_numbers} números necessários')
        elif len(numbers) > config.max_bet_numbers:
            errors.append(f'Máximo de {config.max_bet_numbers} números permitidos')
        
        # Check range
        invalid = [n for n in numbers if n < 1 or n > config.total_numbers]
        if invalid:
            errors.append(f'Números fora do intervalo válido (1-{config.total_numbers}): {invalid}')
        
        # Check duplicates
        if len(numbers) != len(set(numbers)):
            errors.append('Números duplicados encontrados')
        
        # Warnings for patterns
        if len(set(numbers)) == len(numbers):  # Only if no duplicates
            # Check for sequential numbers
            sorted_nums = sorted(numbers)
            sequences = 0
            for i in range(len(sorted_nums) - 1):
                if sorted_nums[i + 1] - sorted_nums[i] == 1:
                    sequences += 1
            
            if sequences > len(numbers) * 0.6:
                warnings.append('Muitos números sequenciais. Isso é raro nos sorteios.')
            
            # Check for same ending digit
            endings = [n % 10 for n in numbers]
            most_common_ending = max(set(endings), key=endings.count)
            if endings.count(most_common_ending) > len(numbers) * 0.5:
                warnings.append(f'Muitos números terminam com {most_common_ending}')
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }


class ResultCheckerService:
    """Service for checking combinations against draw results."""
    
    @staticmethod
    def check_combination(
        lottery_type: str,
        numbers: List[int],
        contest_number: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Check a combination against a draw result.
        
        Args:
            lottery_type: Type of lottery
            numbers: Numbers to check
            contest_number: Specific contest to check (None = latest)
            
        Returns:
            Dictionary with check results
        """
        if contest_number:
            draw = Draw.objects.filter(
                lottery_type=lottery_type,
                contest_number=contest_number
            ).first()
        else:
            draw = Draw.objects.filter(
                lottery_type=lottery_type
            ).order_by('-contest_number').first()
        
        if not draw:
            return {
                'found': False,
                'message': 'Nenhum sorteio encontrado'
            }
        
        drawn_numbers = set(draw.get_numbers_display())
        user_numbers = set(numbers)
        matches = drawn_numbers & user_numbers
        
        return {
            'found': True,
            'contest_number': draw.contest_number,
            'draw_date': draw.draw_date,
            'drawn_numbers': sorted(list(drawn_numbers)),
            'user_numbers': sorted(list(user_numbers)),
            'matches': sorted(list(matches)),
            'match_count': len(matches),
            'is_winner': ResultCheckerService._is_winner(lottery_type, len(matches))
        }
    
    @staticmethod
    def _is_winner(lottery_type: str, match_count: int) -> bool:
        """Determine if match count is a winning combination."""
        # Simplified logic - would need actual prize tiers
        winning_thresholds = {
            'MEGA_SENA': 4,      # Quadra, Quina, Sena
            'LOTOFACIL': 11,     # 11, 12, 13, 14, 15
            'QUINA': 2,          # Duque, Terno, Quadra, Quina
            'DUPLA_SENA': 3,     # Terno, Quadra, Quina, Sena
            'SUPER_SETE': 3,     # 3+ columns
        }
        return match_count >= winning_thresholds.get(lottery_type, 4)
