
  # Drinkpioneer Mobile App UI (라이트모드 추가)

  This is a code bundle for Drinkpioneer Mobile App UI (라이트모드 추가). The original project is available at https://www.figma.com/design/Rh2OlCZtpszZLWa9S00K8R/Drinkpioneer-Mobile-App-UI--%EB%9D%BC%EC%9D%B4%ED%8A%B8%EB%AA%A8%EB%93%9C-%EC%B6%94%EA%B0%80-.

  UI 실행 웹 링크
  https://wager-write-01644490.figma.site

  ## Running the code

  Run `npm i` to install the dependencies.

  Run `npm run dev` to start the development server.


📋 [수정본] Drinkpioneer MVP 개발 인계 프롬프트
다른 개발자나 AI에게 작업을 지시할 때, 아래 내용을 복사해서 가장 먼저 입력해 주세요.

[Project Context]
우리는 **'Drinkpioneer'**라는 앱의 MVP 백엔드를 개발 중입니다. 기존의 단순 주류 상품 조회 기능은 폐기하고, 다음 두 가지 핵심 기능으로 피벗(Pivot)했습니다.

Cocktail Recipe: 사용자가 다양한 칵테일 레시피와 재료 정보를 확인할 수 있는 기능.

Map-based Bar Review: 지도(위도/경도 기반)를 활용하여 오프라인 바(Bar)의 위치를 확인하고 리뷰를 남기는 기능.

[Tech Stack]

Language: Python 3.13

Framework: FastAPI

Database: PostgreSQL (Local host)

ORM: SQLAlchemy (Sync Session)

Validation: Pydantic v2

Server: Uvicorn

[Current Status & Architecture]

Infrastructure (완료): app/core/database.py와 config.py를 통해 DB 연결 및 세션 관리(get_db)가 완벽히 구축되어 있습니다. expire_on_commit=False가 적용되어 세션 에러를 방어합니다.

Legacy Models: 현재 app/models/product.py에 Product 모델이 있으나, 이는 피벗 전 모델이므로 참고만 하거나 향후 칵테일의 '기주(Base Liquor)' 데이터용으로만 축소 사용할 예정입니다.

[To-Be Database Modeling (요구사항)]
새로운 피벗 방향에 맞춰 다음 모델들의 설계와 API 개발이 필요합니다.

Cocktail Model: 칵테일 이름, 기주(Base), 재료 목록, 조리법(Instructions), 난이도 등.

Bar Model: 바 이름, 주소, 위도(Latitude), 경도(Longitude), 영업시간 등. (향후 PostGIS 도입도 고려하나, MVP는 Float 타입의 위/경도로 구현)

Review Model: Bar와 1:N 관계. 별점(Rating), 텍스트 리뷰, 작성자 정보.

[Instructions for Next Steps]
위의 프로젝트 컨텍스트를 바탕으로 개발을 이어나가야 합니다. 다음 원칙을 지켜주세요.

Layered Architecture: Model(DB), Schema(Pydantic), Service(Business Logic), API(Router) 계층을 엄격히 분리하세요.

Spatial Query Preparation: 지도 서비스를 위해 Bar 데이터를 위/경도로 검색할 수 있는 쿼리(예: 특정 좌표 반경 N km 이내 검색) 작성을 염두에 두세요.

Step-by-Step: 한 번에 모든 것을 짜지 말고, 도메인별(Cocktail -> Bar -> Review)로 순차적으로 코드를 제안하세요.

지금부터 위 컨텍스트를 완벽히 숙지하고, 가장 먼저 Cocktail과 Bar에 대한 SQLAlchemy Model (app/models/domain.py 등)과 Pydantic Schema 코드를 작성해 줘.
