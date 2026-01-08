#!/usr/bin/env python3
"""
Generate sample draw data for testing
"""
import sys
import random
from datetime import datetime, timedelta
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models import Draw, LotteryConfiguration
from app.services import StatisticsService


def generate_sample_draws(lottery_type: str, count: int = 100):
    """Generate sample draw data"""
    db = SessionLocal()
    
    try:
        # Get lottery config
        config = db.query(LotteryConfiguration).filter(
            LotteryConfiguration.lottery_type == lottery_type
        ).first()
        
        if not config:
            print(f"❌ Lottery configuration not found: {lottery_type}")
            return
        
        print(f"Generating {count} sample draws for {lottery_type}...")
        
        # Generate draws
        start_date = datetime.now() - timedelta(days=count * 3)
        
        for i in range(count):
            contest_number = 3000 + i
            draw_date = start_date + timedelta(days=i * 3)
            
            # Generate random numbers
            numbers = sorted(random.sample(
                range(1, config.total_numbers + 1),
                config.numbers_to_pick
            ))
            
            # Check if already exists
            existing = db.query(Draw).filter(
                Draw.lottery_type == lottery_type,
                Draw.contest_number == contest_number
            ).first()
            
            if not existing:
                draw = Draw(
                    lottery_type=lottery_type,
                    contest_number=contest_number,
                    draw_date=draw_date.date(),
                    numbers=numbers,
                    prize_amount=random.randint(1000000, 100000000),
                    winners_count=random.randint(0, 5),
                    accumulated=random.choice([True, False]),
                    next_estimated_prize=random.randint(2000000, 150000000)
                )
                db.add(draw)
        
        db.commit()
        print(f"✅ Generated {count} draws for {lottery_type}")
        
        # Calculate statistics
        print(f"Calculating statistics for {lottery_type}...")
        StatisticsService.calculate_statistics(db, lottery_type)
        print(f"✅ Statistics calculated for {lottery_type}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Generate sample data for all lotteries
    lotteries = ['MEGA_SENA', 'LOTOFACIL', 'QUINA', 'DUPLA_SENA', 'SUPER_SETE']
    
    for lottery in lotteries:
        generate_sample_draws(lottery, count=50)
    
    print("\n✅ All sample data generated successfully!")
