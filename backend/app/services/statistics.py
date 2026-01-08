"""
Statistics calculation service
Migrated from Django services
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import Draw, NumberStatistics, LotteryConfiguration
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class StatisticsService:
    """Service for calculating and retrieving lottery statistics"""
    
    @staticmethod
    def calculate_statistics(db: Session, lottery_type: str) -> None:
        """Calculate statistics for all numbers of a lottery type"""
        logger.info(f"Calculating statistics for {lottery_type}")
        
        # Get lottery configuration
        config = db.query(LotteryConfiguration).filter(
            LotteryConfiguration.lottery_type == lottery_type
        ).first()
        
        if not config:
            logger.error(f"Configuration not found for {lottery_type}")
            return
        
        # Get all draws for this lottery
        draws = db.query(Draw).filter(
            Draw.lottery_type == lottery_type
        ).order_by(desc(Draw.contest_number)).all()
        
        if not draws:
            logger.warning(f"No draws found for {lottery_type}")
            return
        
        latest_contest = draws[0].contest_number
        
        # Calculate statistics for each number
        for number in range(1, config.total_numbers + 1):
            frequency = 0
            last_contest = None
            delays = []
            
            # Count frequency and track delays
            for draw in reversed(draws):
                if number in draw.numbers:
                    frequency += 1
                    if last_contest is None:
                        last_contest = draw.contest_number
                    
                    if len(delays) > 0:
                        delays.append(0)
                    delays.append(0)
                else:
                    if delays:
                        delays[-1] += 1
            
            # Calculate delay metrics
            current_delay = latest_contest - last_contest if last_contest else latest_contest
            max_delay = max(delays) if delays else 0
            avg_delay = sum(delays) / len(delays) if delays else 0.0
            
            # Update or create statistics
            stat = db.query(NumberStatistics).filter(
                NumberStatistics.lottery_type == lottery_type,
                NumberStatistics.number == number
            ).first()
            
            if stat:
                stat.frequency = frequency
                stat.last_draw_contest = last_contest
                stat.delay = current_delay
                stat.max_delay = max_delay
                stat.average_delay = avg_delay
            else:
                stat = NumberStatistics(
                    lottery_type=lottery_type,
                    number=number,
                    frequency=frequency,
                    last_draw_contest=last_contest,
                    delay=current_delay,
                    max_delay=max_delay,
                    average_delay=avg_delay
                )
                db.add(stat)
        
        db.commit()
        logger.info(f"Statistics calculated successfully for {lottery_type}")
    
    @staticmethod
    def get_statistics(
        db: Session,
        lottery_type: str,
        limit: Optional[int] = None
    ) -> List[NumberStatistics]:
        """Get statistics for a lottery type"""
        query = db.query(NumberStatistics).filter(
            NumberStatistics.lottery_type == lottery_type
        ).order_by(NumberStatistics.number)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def get_most_frequent(
        db: Session,
        lottery_type: str,
        limit: int = 10
    ) -> List[NumberStatistics]:
        """Get most frequent numbers"""
        return db.query(NumberStatistics).filter(
            NumberStatistics.lottery_type == lottery_type
        ).order_by(desc(NumberStatistics.frequency)).limit(limit).all()
    
    @staticmethod
    def get_most_delayed(
        db: Session,
        lottery_type: str,
        limit: int = 10
    ) -> List[NumberStatistics]:
        """Get most delayed numbers"""
        return db.query(NumberStatistics).filter(
            NumberStatistics.lottery_type == lottery_type
        ).order_by(desc(NumberStatistics.delay)).limit(limit).all()
