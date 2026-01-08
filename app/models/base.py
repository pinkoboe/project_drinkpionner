# app/models/base.py
# v3.0 스키마 파일에서 정의한 Base 클래스와 모든 모델을 이곳으로 가져옵니다.
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# 명세서 v3.0의 모든 모델 클래스(User, Product, Bar 등)를 
# 이 파일에서 import 해두어야 Alembic이 테이블 변화를 감지할 수 있습니다.