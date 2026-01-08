#!/usr/bin/env python3
"""
Initialize database with lottery configurations
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models import LotteryConfiguration


def init_lotteries():
    """Initialize lottery configurations"""
    db = SessionLocal()
    
    lotteries = [
        LotteryConfiguration(
            lottery_type='MEGA_SENA',
            total_numbers=60,
            numbers_to_pick=6,
            min_bet_numbers=6,
            max_bet_numbers=20,
            primary_color='#209869',
            description='Escolha 6 números de 1 a 60. Sorteios às quartas e sábados.'
        ),
        LotteryConfiguration(
            lottery_type='LOTOFACIL',
            total_numbers=25,
            numbers_to_pick=15,
            min_bet_numbers=15,
            max_bet_numbers=20,
            primary_color='#930089',
            description='Escolha 15 números de 1 a 25. Sorteios de segunda a sábado.'
        ),
        LotteryConfiguration(
            lottery_type='QUINA',
            total_numbers=80,
            numbers_to_pick=5,
            min_bet_numbers=5,
            max_bet_numbers=15,
            primary_color='#260085',
            description='Escolha 5 números de 1 a 80. Sorteios de segunda a sábado.'
        ),
        LotteryConfiguration(
            lottery_type='DUPLA_SENA',
            total_numbers=50,
            numbers_to_pick=6,
            min_bet_numbers=6,
            max_bet_numbers=15,
            primary_color='#A61324',
            description='Escolha 6 números de 1 a 50. Duas chances de ganhar. Sorteios às terças, quintas e sábados.'
        ),
        LotteryConfiguration(
            lottery_type='SUPER_SETE',
            total_numbers=10,
            numbers_to_pick=7,
            min_bet_numbers=7,
            max_bet_numbers=21,
            primary_color='#A8CF45',
            description='Escolha 7 colunas de 0 a 9. Sorteios às segundas, quartas e sextas.'
        ),
    ]
    
    try:
        for lottery in lotteries:
            # Check if exists
            existing = db.query(LotteryConfiguration).filter(
                LotteryConfiguration.lottery_type == lottery.lottery_type
            ).first()
            
            if existing:
                # Update
                existing.total_numbers = lottery.total_numbers
                existing.numbers_to_pick = lottery.numbers_to_pick
                existing.min_bet_numbers = lottery.min_bet_numbers
                existing.max_bet_numbers = lottery.max_bet_numbers
                existing.primary_color = lottery.primary_color
                existing.description = lottery.description
                print(f"✓ Updated: {lottery.lottery_type}")
            else:
                # Create
                db.add(lottery)
                print(f"✓ Created: {lottery.lottery_type}")
        
        db.commit()
        print("\n✅ Lotteries initialized successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_lotteries()
