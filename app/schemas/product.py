from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FlavorProfileCreate(BaseModel):
    aroma_score: float  # 0-10
    aroma_notes: str
    taste_score: float
    taste_notes: str
    finish_score: float
    finish_notes: str

class ProductCreate(BaseModel):
    name: str
    brand: str
    category_id: int
    abv: Optional[float] = None
    latest_price: int
    price_source: str = "초기등록"
    flavor_profile: FlavorProfileCreate

class ProductResponse(BaseModel):
    id: int
    name: str
    latest_price: int
    
    class Config:
        from_attributes = True