"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal


class LotteryConfigBase(BaseModel):
    lottery_type: str
    total_numbers: int
    numbers_to_pick: int
    min_bet_numbers: Optional[int] = None
    max_bet_numbers: Optional[int] = None
    primary_color: str = "#009B3A"
    description: str = ""


class LotteryConfigCreate(LotteryConfigBase):
    pass


class LotteryConfig(LotteryConfigBase):
    id: int
    
    class Config:
        from_attributes = True


class DrawBase(BaseModel):
    lottery_type: str
    contest_number: int
    draw_date: date
    numbers: List[int]
    numbers_second_draw: Optional[List[int]] = None
    prize_amount: Optional[Decimal] = None
    winners_count: Optional[int] = 0
    accumulated: bool = False
    next_estimated_prize: Optional[Decimal] = None


class DrawCreate(DrawBase):
    pass


class Draw(DrawBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class NumberStatisticsBase(BaseModel):
    lottery_type: str
    number: int
    frequency: int = 0
    last_draw_contest: Optional[int] = None
    delay: int = 0
    max_delay: int = 0
    average_delay: float = 0.0


class NumberStatistics(NumberStatisticsBase):
    id: int
    last_updated: datetime
    
    class Config:
        from_attributes = True


class UserCombinationBase(BaseModel):
    lottery_type: str
    name: str = ""
    numbers: List[int]
    is_favorite: bool = False


class UserCombinationCreate(UserCombinationBase):
    session_key: Optional[str] = None


class UserCombination(UserCombinationBase):
    id: int
    session_key: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GeneratorRequest(BaseModel):
    lottery_type: str
    numbers_count: int = Field(ge=6, le=20)
    games_count: int = Field(ge=1, le=50)
    fixed_numbers: Optional[List[int]] = None
    include_frequent: bool = False
    include_delayed: bool = False
    mix_strategy: bool = True


class GeneratorResponse(BaseModel):
    lottery_type: str
    combinations: List[List[int]]
    metadata: dict


class CheckerRequest(BaseModel):
    lottery_type: str
    numbers: List[int]
    contest_number: Optional[int] = None


class CheckerResponse(BaseModel):
    found: bool
    contest_number: Optional[int] = None
    draw_date: Optional[date] = None
    drawn_numbers: Optional[List[int]] = None
    user_numbers: List[int]
    matches: List[int]
    match_count: int
    is_winner: bool
