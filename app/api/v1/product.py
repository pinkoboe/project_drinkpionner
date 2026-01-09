from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.product_service import get_products, get_product_by_id
from app.schemas.product import ProductResponse, ProductDetailResponse

router = APIRouter()

@router.get("/", response_model=List[ProductResponse])
def read_products(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    """
    모든 상품 목록 조회 (페이징)
    """
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=ProductDetailResponse)
def read_product(
    product_id: int, 
    db: Session = Depends(get_db)
):
    """
    특정 상품 상세 조회 (가격 이력 포함)
    """
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
    return product