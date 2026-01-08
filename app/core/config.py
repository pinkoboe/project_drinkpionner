from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


def _read_env_file_safely(env_file_path: str) -> dict:
    """
    .env 파일을 여러 인코딩으로 시도해서 읽어서 안전하게 파싱합니다.
    Windows에서 CP949로 저장된 경우도 처리합니다.
    """
    env_vars = {}
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr', 'latin-1']
    
    if not os.path.exists(env_file_path):
        return env_vars
    
    for encoding in encodings:
        try:
            with open(env_file_path, 'r', encoding=encoding) as f:
                for line in f:
                    line = line.strip()
                    # 주석이나 빈 줄 건너뛰기
                    if not line or line.startswith('#'):
                        continue
                    # KEY=VALUE 형식 파싱
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # 따옴표 제거
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        env_vars[key] = value
            # 성공적으로 읽었으면 중단
            break
        except (UnicodeDecodeError, UnicodeError):
            # 이 인코딩으로 읽기 실패, 다음 인코딩 시도
            continue
        except Exception:
            # 다른 에러는 무시하고 다음 인코딩 시도
            continue
    
    return env_vars


class Settings(BaseSettings):
    PROJECT_NAME: str = "Drinkpioneer API"
    API_V1_STR: str = "/api/v1"
    
    # DB 관련 설정
    DATABASE_URL: str

    # extra="ignore" 추가 -> .env에 있는 다른 변수들은 에러 내지 말고 무시하라는 뜻
    model_config = SettingsConfigDict(extra="ignore")
    
    def __init__(self, **kwargs):
        # .env 파일을 직접 읽어서 안전하게 처리
        env_file_path = Path(".env")
        if env_file_path.exists():
            env_vars = _read_env_file_safely(str(env_file_path))
            # 환경변수와 .env 파일 내용 병합 (환경변수가 우선)
            for key, value in env_vars.items():
                if key not in os.environ:
                    os.environ[key] = value
        
        super().__init__(**kwargs)
        
        # DATABASE_URL을 안전하게 정규화 (인코딩 문제 방지)
        if hasattr(self, 'DATABASE_URL') and self.DATABASE_URL:
            try:
                # 이미 깨진 문자열이 들어왔을 수 있으므로, 
                # latin-1로 디코딩 후 UTF-8로 재인코딩하는 방식으로 복구 시도
                if isinstance(self.DATABASE_URL, str):
                    # 문자열을 latin-1 바이트로 변환 후 UTF-8로 디코딩
                    try:
                        # 먼저 UTF-8로 정상 디코딩 시도
                        test_bytes = self.DATABASE_URL.encode('utf-8')
                        normalized = test_bytes.decode('utf-8')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        # UTF-8로 인코딩 실패 시, latin-1을 거쳐서 복구 시도
                        normalized = self.DATABASE_URL.encode('latin-1', errors='ignore').decode('utf-8', errors='ignore')
                    
                    # 공백 제거 및 정리
                    normalized = normalized.strip()
                    # ASCII가 아닌 문자가 있는지 확인하고 제거
                    normalized = ''.join(char if ord(char) < 128 or char.isprintable() else '' for char in normalized)
                    object.__setattr__(self, 'DATABASE_URL', normalized)
            except Exception:
                # 정규화 실패 시 원본 유지
                pass

settings = Settings()