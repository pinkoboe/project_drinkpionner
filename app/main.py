from fastapi import FastAPI
from app.models.base import Base
from app.core.database import engine
# [추가 1] 만든 API 라우터 불러오기
from app.api.v1.admin import product as admin_product
from app.core.config import settings

# [추가 2] 모델들이 로드되도록 임포트 (테이블 생성을 위해 필수)
# app/models/__init__.py가 잘 작성되어 있다고 가정합니다.
# 만약 에러가 난다면 from app.models.product import Product 처럼 직접 적어주세요.
import app.models

app = FastAPI(title="Drinkpioneer API")


@app.on_event("startup")
def on_startup() -> None:
    """
    서버 시작 시점에 한 번만 테이블 생성 및 DB 연결 검증을 수행한다.
    인코딩 문제나 설정 오류가 있으면 여기서 명확한 메시지와 함께 실패하게 한다.
    """
    try:
        Base.metadata.create_all(bind=engine)
    except UnicodeDecodeError as e:
        # psycopg2가 DSN 처리 중 터지는 경우를 좀 더 이해하기 쉬운 메시지로 변환
        raise RuntimeError(
            "DB 초기화 중 인코딩 오류가 발생했습니다. DATABASE_URL에 한글/특수문자가 포함되었다면 "
            "영문/숫자 위주로 바꾸거나 URL 인코딩해서 다시 설정해 주세요."
        ) from e
    except Exception as e:
        # 다른 예외는 일괄적으로 설정 문제로 안내
        raise RuntimeError(
            f"DB 초기화에 실패했습니다. DATABASE_URL 및 DB 서버 상태를 확인해 주세요. 원인: {e}"
        ) from e


# [추가 3] 라우터 등록 (이게 있어야 URL이 동작함)
app.include_router(
    admin_product.router,
    prefix=f"{settings.API_V1_STR}/admin/products",
    tags=["admin-products"],
)


@app.get("/")
def read_root():
    return {"message": "Drinkpioneer 서버가 정상 작동 중입니다!"}

