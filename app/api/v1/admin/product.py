from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import create_product_with_details

router = APIRouter()

@router.post("/", response_model=ProductResponse)
def register_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db)
):
    """
    관리자가 주류 마스터 데이터를 등록합니다.
    이때 맛 프로필과 초기 가격 이력이 동시에 생성됩니다.
    """
    return create_product_with_details(db, obj_in=product_in)