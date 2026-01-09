from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict
from datetime import datetime

# [기존] 맛 데이터
class FlavorProfileCreate(BaseModel):
    aroma_score: float
    aroma_notes: str
    taste_score: float
    taste_notes: str
    finish_score: float
    finish_notes: str

# [기존] 상품 생성 요청
class ProductCreate(BaseModel):
    name: str
    brand: str
    category_id: int
    abv: Optional[float] = None
    latest_price: int
    price_source: str = "초기등록"
    flavor_profile: FlavorProfileCreate

# [기존 수정] 상품 목록 응답 (기본 정보)
class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    category_id: int
    abv: Optional[float]
    latest_price: int
    
    # Pydantic v2 설정 (ORM 객체 변환 허용)
    model_config = ConfigDict(from_attributes=True)

# [신규 추가] 가격 이력 응답
class PriceHistoryResponse(BaseModel):
    id: int
    price: int
    source: str
    date: datetime

    model_config = ConfigDict(from_attributes=True)

# [신규 추가] 상품 상세 응답 (가격 이력 포함)
class ProductDetailResponse(ProductResponse):
    # ProductResponse의 필드를 모두 상속받고, 가격 이력 리스트를 추가
    price_history: List[PriceHistoryResponse] = []