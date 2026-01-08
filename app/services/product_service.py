from sqlalchemy.orm import Session
from app.models import Product, Review, PriceHistory # v3.0 모델 참조
from app.schemas.product import ProductCreate
from datetime import datetime

def create_product_with_details(db: Session, obj_in: ProductCreate):
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

    # 2. 가격 이력 생성 (v3.0 전략 반영)
    db_price = PriceHistory(
        product_id=db_product.id,
        price=obj_in.latest_price,
        source=obj_in.price_source,
        date=datetime.utcnow()
    )
    db.add(db_price)

    # 3. 맛 프로필 생성 (v3.0 상세화 반영)
    # 실제 앱에서는 제품 등록 시 시스템 리뷰 형태로 맛 데이터를 관리자 계정으로 저장합니다.
    # (여기서는 예시를 위해 단순화된 저장 로직을 적용)
    
    db.commit()
    db.refresh(db_product)
    return db_product