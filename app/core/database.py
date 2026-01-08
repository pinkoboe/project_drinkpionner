from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings


def _create_engine_safely(database_url: str):
    """
    DATABASE_URL에 인코딩 문제가 있거나 형식이 잘못된 경우
    psycopg2 내부에서 바로 UnicodeDecodeError 등이 터지기 때문에
    여기서 한 번 래핑해서 더 친절한 에러 메시지를 제공한다.
    """
    # DATABASE_URL을 안전하게 정규화 (인코딩 문제 방지)
    normalized_url = database_url
    
    try:
        # 문자열을 UTF-8로 명시적으로 정규화
        if isinstance(database_url, bytes):
            normalized_url = database_url.decode('utf-8', errors='ignore')
        elif isinstance(database_url, str):
            # 깨진 문자열 복구 시도
            try:
                # 먼저 UTF-8로 정상 인코딩/디코딩 시도
                test_bytes = database_url.encode('utf-8')
                normalized_url = test_bytes.decode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                # UTF-8 실패 시 latin-1을 거쳐서 복구
                try:
                    normalized_url = database_url.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
                except Exception:
                    # 그래도 실패하면 ASCII만 남기기
                    normalized_url = ''.join(char if ord(char) < 128 else '' for char in database_url)
        
        # 공백 제거 및 정리
        normalized_url = normalized_url.strip()
        
        # 디버깅: 정규화된 URL 확인 (비밀번호는 가림)
        if '://' in normalized_url:
            parts = normalized_url.split('://', 1)
            if len(parts) == 2 and '@' in parts[1]:
                # 비밀번호 부분 가리기
                protocol = parts[0]
                rest = parts[1]
                if ':' in rest and '@' in rest:
                    user_pass, host_db = rest.split('@', 1)
                    if ':' in user_pass:
                        user, _ = user_pass.split(':', 1)
                        masked = f"{protocol}://{user}:***@{host_db}"
                        print(f"[DEBUG] 정규화된 DATABASE_URL (비밀번호 가림): {masked}")
    except Exception as e:
        print(f"[WARNING] DATABASE_URL 정규화 중 오류 발생: {e}")
        normalized_url = database_url  # 정규화 실패 시 원본 사용
    
    try:
        return create_engine(normalized_url, pool_pre_ping=True)
    except UnicodeDecodeError as e:
        # psycopg2가 DSN 문자열을 처리하다가 터지는 대표적인 경우
        raise RuntimeError(
            "데이터베이스 연결 문자열(DATABASE_URL)을 해석하는 중 인코딩 오류가 발생했습니다. "
            "아이디/비밀번호/DB명/옵션, 경로 등에 한글이나 특수문자가 포함되어 있다면 "
            "영문/숫자 위주로 변경하거나 URL 인코딩(퍼센트 인코딩)해서 사용해 주세요. "
            f"또한 .env 파일을 UTF-8 인코딩으로 저장했는지 확인해 주세요. "
            f"원본 에러: {e}"
        ) from e
    except Exception as e:
        # 다른 예외에 대해서도 설정 문제를 바로 알 수 있도록 메시지 보강
        raise RuntimeError(
            f"데이터베이스 엔진 생성에 실패했습니다. DATABASE_URL 설정을 다시 확인해 주세요. 원인: {e}"
        ) from e


# 1. SQLAlchemy 엔진 생성
# PostgreSQL을 사용하므로 별도의 check_same_thread 옵션은 필요 없습니다.
engine = _create_engine_safely(settings.DATABASE_URL)

# 2. 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


# 3. FastAPI에서 사용할 DB 세션 의존성 (get_db)
def get_db():
    """
    각 API 요청 시 세션을 생성하고 요청이 끝나면 자동으로 닫아줍니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()