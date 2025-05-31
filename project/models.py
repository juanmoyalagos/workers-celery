from pydantic import BaseModel

class Number(BaseModel):
    number: int

class StockEstimation(BaseModel):
    current_price: float
    last_month_price: float
    day_difference: float
    shares_count: int
