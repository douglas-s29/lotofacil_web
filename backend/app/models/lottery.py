"""
SQLAlchemy models for lottery application
Migrated from Django models
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, Text, Numeric, Index, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum


class LotteryType(str, enum.Enum):
    """Lottery types supported by the system"""
    MEGA_SENA = "MEGA_SENA"
    LOTOFACIL = "LOTOFACIL"
    QUINA = "QUINA"
    DUPLA_SENA = "DUPLA_SENA"
    SUPER_SETE = "SUPER_SETE"


class LotteryConfiguration(Base):
    """Configuration for each lottery type"""
    __tablename__ = "lottery_configuration"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_type = Column(String(20), unique=True, nullable=False, index=True)
    total_numbers = Column(Integer, nullable=False)
    numbers_to_pick = Column(Integer, nullable=False)
    min_bet_numbers = Column(Integer, nullable=True)
    max_bet_numbers = Column(Integer, nullable=True)
    primary_color = Column(String(7), default="#009B3A")
    description = Column(Text, default="")
    
    def __repr__(self):
        return f"<LotteryConfiguration {self.lottery_type}>"


class Draw(Base):
    """Historical draw/contest results"""
    __tablename__ = "draw"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_type = Column(String(20), nullable=False, index=True)
    contest_number = Column(Integer, nullable=False, index=True)
    draw_date = Column(Date, nullable=False, index=True)
    numbers = Column(JSON, nullable=False)
    numbers_second_draw = Column(JSON, nullable=True)
    prize_amount = Column(Numeric(15, 2), nullable=True)
    winners_count = Column(Integer, default=0)
    accumulated = Column(Boolean, default=False)
    next_estimated_prize = Column(Numeric(15, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_lottery_contest', 'lottery_type', 'contest_number', unique=True),
        Index('idx_lottery_date', 'lottery_type', 'draw_date'),
    )
    
    def __repr__(self):
        return f"<Draw {self.lottery_type} Contest {self.contest_number}>"


class NumberStatistics(Base):
    """Cached statistics for lottery numbers"""
    __tablename__ = "number_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_type = Column(String(20), nullable=False, index=True)
    number = Column(Integer, nullable=False)
    frequency = Column(Integer, default=0)
    last_draw_contest = Column(Integer, nullable=True)
    delay = Column(Integer, default=0)
    max_delay = Column(Integer, default=0)
    average_delay = Column(Float, default=0.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_lottery_number', 'lottery_type', 'number', unique=True),
        Index('idx_lottery_frequency', 'lottery_type', 'frequency'),
        Index('idx_lottery_delay', 'lottery_type', 'delay'),
    )
    
    def __repr__(self):
        return f"<NumberStatistics {self.lottery_type} Number {self.number}>"


class UserCombination(Base):
    """User saved combinations"""
    __tablename__ = "user_combination"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_type = Column(String(20), nullable=False, index=True)
    name = Column(String(200), default="")
    numbers = Column(JSON, nullable=False)
    session_key = Column(String(40), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_favorite = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<UserCombination {self.name}>"


class GenerationFilter(Base):
    """Saved filter configurations for combination generation"""
    __tablename__ = "generation_filter"
    
    id = Column(Integer, primary_key=True, index=True)
    lottery_type = Column(String(20), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    filter_config = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<GenerationFilter {self.name}>"
