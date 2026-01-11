from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from app.models import Product, Review, PriceHistory
from app.schemas.product import ProductCreate

def create_product_with_details(db: Session, obj_in: ProductCreate):
    """
    상품 등록 로직 (트랜잭션)
    """
    # 1. 제품 기본 정보 생성
    db_product = Product(
        name=obj_in.name,
        brand=obj_in.brand,
        category_id=obj_in.category_id,
        abv=obj_in.abv,
        latest_price=obj_in.latest_price,
        price_updated_at=datetime.utcnow()
    )
    db.add(db_product)
    db.flush() # ID를 미리 할당받기 위함

    # 2. 가격 이력 생성
    db_price = PriceHistory(
        product_id=db_product.id,
        price=obj_in.latest_price,
        source=obj_in.price_source,
        date=datetime.utcnow()
    )
    db.add(db_price)

    # 3. 맛 프로필 등 추가 로직이 있다면 여기에 작성
    
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session, skip: int = 0, limit: int = 10):
    """
    모든 상품 목록 조회 (페이징)
    """
    stmt = select(Product).offset(skip).limit(limit)
    result = db.execute(stmt)
    return result.scalars().all()

def get_product_by_id(db: Session, product_id: int):
    """
    상품 상세 조회 (가격 이력 포함)
    """
    # [수정] Product.price_histories -> Product.price_history (모델 정의와 일치시킴)
    stmt = (
        select(Product)
        .options(selectinload(Product.price_history)) 
        .where(Product.id == product_id)
    )
    result = db.execute(stmt)
    return result.scalar_one_or_none()