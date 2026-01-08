from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, index=True)
    category_id = Column(Integer, nullable=False)  # 실제로는 Category 모델과 FK 연결 가능
    abv = Column(Float)
    latest_price = Column(Integer)
    price_updated_at = Column(DateTime, default=datetime.utcnow)

    # PriceHistory와의 관계 설정 (1:N)
    price_history = relationship("PriceHistory", back_populates="product")

class PriceHistory(Base):
    __tablename__ = "price_histories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Integer, nullable=False)
    source = Column(String, nullable=False) # 예: '마트A', '편의점B'
    date = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")

# 서비스 코드에서 Review를 import 하고 있어서 에러 방지용으로 추가 (나중에 구현)
class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)