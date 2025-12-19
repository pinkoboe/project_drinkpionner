# Drinkpioneer MVP 기능 명세서 (Functional Specification)

> **문서 버전**: v2.0 MVP Edition  
> **작성일**: 2025-12-14  
> **작성자**: PM/시스템 아키텍트  
> **전략**: 실용성(Utility) 최우선 MVP  
> **목적**: Phase 1 핵심 기능 상세 정의 + Phase 2 로드맵

---

## 📋 MVP 전략 개요

### Phase 1: 핵심 개발 기능 (상세 스펙 포함)

1. ✅ **내 술장 (My Cabinet)** - 보유 술 관리 + 2D Grid View
2. ✅ **검색 (Search)** - 주류 검색 + **가격 정보 강조**
3. ✅ **바 지도 (Bar Map)** - 지도 API + 위치 기반 바 찾기
4. ✅ **칵테일 레시피 (Cocktail Recipes)** - 내 술장 기반 추천
5. ✅ **설정/로그인 (Settings/Auth)** - 기본 사용자 관리

### Phase 2: 추후 도입 기능 (요약만)

- 🔮 **AI 블렌딩 랩** - 우선순위 낮춤 (데이터 학습 필요)
- 💬 **커뮤니티** - 사용자 기반 확보 후 도입
- 📊 **가격 추이 그래프** - 가격 데이터 축적 후 도입
- 🎨 **3D 술장 뷰** - 구현 복잡도 고려하여 Phase 2로 연기

---

## 1. 내 술장 (My Cabinet) - HOME_SCREEN

### 1.1 화면 개요

- **화면 ID**: `HOME_001`
- **경로**: `/` (Root Screen)
- **컴포넌트**: `MyCabinetScreen.tsx`
- **주요 기능**: 보유한 술 목록 관리, 칵테일 레시피 추천, 술장 보기 (2D Grid View)
- **MVP 전략**: 3D 뷰는 Phase 2로 연기 (구현 복잡도 고려)

---

### 1.2 기능 명세 테이블

| 화면ID       | 기능명                  | 구분(Trigger)                    | 상세 로직(Logic)                                                                                                                                                                                                                                                                                                                                                                                        | 예외 처리(Exception)                                                                                                                                                                                                                                                                    | 데이터(I/O)                                                                                                                                                                                                                                       |
| ------------ | ----------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HOME_001_F01 | 보유 술 목록 조회       | 화면 진입 시 자동 실행           | 1. `GET /api/cabinet/bottles` 호출<br>2. 헤더에 `Authorization: Bearer {token}` 포함<br>3. 응답 데이터를 `bottles` state에 저장<br>4. 각 술 카드를 Grid 형태로 렌더링 (2열 고정)<br>5. 이미지는 `ImageWithFallback` 컴포넌트 사용<br>6. 카드 정렬: 최신 추가순 (addedAt DESC)                                                                                                                           | **Loading**: Skeleton UI 표시 (6개 카드)<br>**Empty**: "아직 추가한 술이 없어요" 메시지 + "첫 술 추가하기" CTA 버튼<br>**Error**: Toast 메시지 "술 목록을 불러올 수 없습니다" + 재시도 버튼<br>**401 Unauthorized**: 자동 로그인 화면 리다이렉트                                        | **Input**: `Authorization token`<br>**Output**: `Bottle[]`<br>`typescript<br>interface Bottle {<br>  id: string;<br>  name: string;<br>  type: string;<br>  brand: string;<br>  image: string;<br>  abv?: number;<br>  addedAt: string;<br>}<br>` |
| HOME_001_F02 | 새 술 추가 (다이얼로그) | '+' 버튼 클릭                    | 1. `setShowAddBottleDialog(true)` 호출하여 Dialog 오픈<br>2. Dialog 내부 폼 렌더링:<br> - 술 이름 Input (필수)<br> - 브랜드 Input (선택)<br> - 카테고리 Select (Whiskey/Soju/Beer/Wine/Makgeolli)<br> - 도수(ABV) Input (선택, number)<br>3. "추가" 버튼 클릭 시 Validation 수행<br>4. 통과 시 `POST /api/cabinet/bottles` 호출<br>5. 성공 시 Dialog 닫기 + 목록 새로고침 + Toast "술이 추가되었습니다" | **Validation**:<br>- 술 이름 2글자 미만: "술 이름을 2글자 이상 입력해주세요" (Input 하단 에러 텍스트)<br>- 카테고리 미선택: "카테고리를 선택해주세요"<br>- ABV 범위 초과 (0-100): "올바른 도수를 입력해주세요 (0-100)"<br>**API Error**: Toast "추가에 실패했습니다. 다시 시도해주세요" | **Input**:<br>`typescript<br>interface AddBottleRequest {<br>  name: string;<br>  brand?: string;<br>  type: string;<br>  abv?: number;<br>}<br>`<br>**Output**: `{ success: boolean, bottleId: string }`                                         |
| HOME_001_F03 | 술 삭제                 | 술 카드 길게 누르기 (long press) | 1. 1초 이상 터치 시 `AlertDialog` 표시<br>2. "정말 삭제하시겠습니까?" 확인 메시지<br>3. "삭제" 버튼 클릭 시 `DELETE /api/cabinet/bottles/{bottleId}` 호출<br>4. 성공 시 해당 카드 Fade-out 애니메이션 (500ms)<br>5. 목록에서 제거 후 Toast "삭제되었습니다"                                                                                                                                             | **API Error**: Toast "삭제에 실패했습니다" + 카드 복원<br>**네트워크 끊김**: 삭제 취소 + Toast "네트워크 연결을 확인해주세요"                                                                                                                                                           | **Input**: `bottleId` (string)<br>**Output**: `{ success: boolean }`                                                                                                                                                                              |

---

## 2. 검색 (Search) - SEARCH_SCREEN

### 2.1 화면 개요

- **화면 ID**: `SEARCH_001`
- **경로**: `/search`
- **컴포넌트**: `SearchScreen.tsx`
- **주요 기능**: 술 검색, **가격 정보 강조**, 다중 필터, 상세 정보 조회
- **MVP 전략**: 가격 추이 그래프는 Phase 2로 연기 (데이터 축적 필요)

---

### 2.2 기능 명세 테이블

| 화면ID         | 기능명                     | 구분(Trigger)              | 상세 로직(Logic)                                                                                                                                                                                                                                                                                                                            | 예외 처리(Exception)                                                                                                                                                                                                                            | 데이터(I/O)                                                                                                                                                                                                                                                                                                                                                                                        |
| -------------- | -------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SEARCH_001_F01 | 검색어 입력                | Input onChange 이벤트      | 1. 사용자가 Input에 텍스트 입력<br>2. `setSearchQuery(value)` 실행<br>3. **Debounce 300ms** 적용<br>4. 300ms 경과 후 `GET /api/products/search?q={query}` 호출<br>5. 결과를 `filteredProducts` state에 저장<br>6. 검색 결과 카드 렌더링 (2열 Grid)<br>7. **각 카드에 가격 정보를 크고 명확하게 표시**                                       | **2글자 미만 입력 시**: API 호출 안 함, Input 하단에 "2글자 이상 입력해주세요" 회색 안내 텍스트<br>**검색 결과 0개**: "검색 결과가 없습니다" Empty State + 인기 검색어 추천<br>**API Error**: Toast "검색에 실패했습니다" + 이전 검색 결과 유지 | **Input**: `query` (string)<br>**Output**:<br>`typescript<br>interface SearchResult {<br>  products: Product[];<br>  totalCount: number;<br>  suggestedKeywords: string[];<br>}<br>interface Product {<br>  id: string;<br>  name: string;<br>  type: string;<br>  brand: string;<br>  price: number; // ✅ 필수<br>  image: string;<br>  rating: number;<br>  reviews: number;<br>}<br>`          |
| SEARCH_001_F02 | 가격 정보 표시 (강조)      | 검색 결과 렌더링 시 자동   | 1. 각 제품 카드에서 **가격을 제일 눈에 띄게 표시**<br>2. 가격 포맷: `450,000원` (천단위 콤마)<br>3. 가격 아래에 "온라인 최저가 기준" 작은 회색 텍스트<br>4. 가격 정보가 없는 제품은 "가격 문의" Badge 표시<br>5. 카드 레이아웃: 이미지 → 이름/브랜드 → **가격 (강조)** → 평점                                                               | **가격 정보 없음**: "가격 문의" Badge + 제품 상세 페이지에서 "가격 정보를 제공해주세요" CTA<br>**가격 0원**: "무료 샘플" Badge                                                                                                                  | **Display**:<br>`typescript<br>// 가격 표시 우선순위<br>1. price > 0: "450,000원"<br>2. price === 0: "무료 샘플"<br>3. price === null: "가격 문의"<br>`                                                                                                                                                                                                                                            |
| SEARCH_001_F03 | 카테고리 필터              | 카테고리 Badge 클릭        | 1. 상단에 카테고리 Badge 5개 렌더링: [Whiskey, Soju, Beer, Wine, Makgeolli]<br>2. `selectedCategory` state 업데이트<br>3. 선택된 Badge에 `bg-primary` 스타일 적용<br>4. `GET /api/products?category={category}&q={query}` 호출<br>5. 기존 검색 결과를 필터링된 결과로 교체<br>6. 카테고리 변경 시 스크롤을 상단으로 이동                    | **Loading**: 기존 카드들 위에 반투명 Overlay + Spinner<br>**API Error**: 이전 카테고리로 복원 + Toast "필터 적용 실패"                                                                                                                          | **State**: `selectedCategory: "Whiskey" \| "Soju" \| "Beer" \| "Wine" \| "Makgeolli"`                                                                                                                                                                                                                                                                                                              |
| SEARCH_001_F04 | 가격 필터                  | Sheet 내부 Slider 조작     | 1. "필터" 아이콘 버튼 클릭 시 Sheet (Drawer) 오픈<br>2. 가격 범위 Slider 렌더링 (최소: 0원, 최대: 1,000,000원)<br>3. Slider onChange 시 `setPriceRange([min, max])` 실행<br>4. **실시간 필터링은 안 함** (성능 고려)<br>5. "적용" 버튼 클릭 시 `GET /api/products?minPrice={min}&maxPrice={max}` 호출<br>6. Sheet 닫기 + 필터링된 결과 표시 | **Slider 값이 [0, 1000000]과 동일할 때**: "전체 가격" Badge 표시<br>**API Error**: 필터 적용 취소 + Toast "필터 적용 실패"                                                                                                                      | **Input**: `{ minPrice: number, maxPrice: number }`<br>**단위**: 1,000원 (Slider step: 10000)                                                                                                                                                                                                                                                                                                      |
| SEARCH_001_F05 | 음식 페어링 필터           | Badge Toggle               | 1. Sheet 내부 "Food Pairing" 섹션 렌더링<br>2. 각 음식 Badge 클릭 시 `togglePairing(name)` 실행<br>3. 선택된 Badge는 `selectedPairings[]` 배열에 추가<br>4. 최대 3개까지 선택 가능<br>5. "적용" 버튼 클릭 시 `GET /api/products?pairings={comma-separated}` 호출                                                                            | **3개 초과 선택 시**: Toast "페어링은 최대 3개까지 선택 가능합니다" + 마지막 선택 취소                                                                                                                                                          | **State**: `selectedPairings: string[]` (최대 3개)<br>**Options**: ["Steak", "Cheese", "Sashimi", "Chocolate", "Nuts"]                                                                                                                                                                                                                                                                             |
| SEARCH_001_F06 | 제품 상세 보기             | 제품 카드 클릭             | 1. 제품 카드 클릭 시 `setSelectedProduct(product)` 실행<br>2. Full Screen Dialog 렌더링<br>3. `GET /api/products/{productId}` 호출하여 상세 정보 로드<br>4. 제품 이미지, 이름, 타입, **가격 (크게 강조)**, 평점 표시<br>5. "Nose/Palate/Finish" 점수를 막대 그래프로 시각화<br>6. "내 술장에 추가" 버튼 표시                                | **Loading**: Dialog 내부 Skeleton<br>**API Error**: "제품 정보를 불러올 수 없습니다" + Dialog 자동 닫기 (2초 후)                                                                                                                                | **Input**: `productId` (string)<br>**Output**:<br>`typescript<br>interface ProductDetail {<br>  id: string;<br>  name: string;<br>  type: string;<br>  brand: string;<br>  price: number; // ✅ 강조<br>  rating: number;<br>  reviews: number;<br>  image: string;<br>  ratings: {<br>    nose: number;<br>    palate: number;<br>    finish: number;<br>  };<br>  description: string;<br>}<br>` |
| SEARCH_001_F07 | 내 술장에 추가 (Quick Add) | 상세 Dialog 내부 버튼 클릭 | 1. "내 술장에 추가" 버튼 클릭<br>2. `POST /api/cabinet/bottles` 호출<br> - 제품 정보를 그대로 전달 (name, type, brand, image)<br>3. 성공 시 Toast "내 술장에 추가되었습니다" + 체크 아이콘<br>4. 버튼 텍스트 변경: "추가됨" (Disabled 상태)                                                                                                 | **이미 추가된 제품**: 버튼 텍스트 "이미 추가됨" (Disabled)<br>**API Error**: Toast "추가 실패. 다시 시도해주세요"<br>**401 Unauthorized**: "로그인이 필요합니다" Toast + 로그인 화면 제안                                                       | **Input**:<br>`typescript<br>interface QuickAddRequest {<br>  productId: string;<br>  name: string;<br>  type: string;<br>  brand: string;<br>  image: string;<br>}<br>`<br>**Output**: `{ success: boolean, bottleId: string }`                                                                                                                                                                   |

---

## 3. 바 지도 (Bar Map) - BAR_MAP_SCREEN ⭐

### 3.1 화면 개요

- **화면 ID**: `MAP_001`
- **경로**: `/map`
- **컴포넌트**: `BarMapScreen.tsx`
- **주요 기능**: 지도 API 연동, 내 위치 기반 바 찾기, 바 상세 정보 (보유 주류)
- **지도 API**: Google Maps API 또는 Naver Maps API 사용

---

### 3.2 기능 명세 테이블

| 화면ID      | 기능명              | 구분(Trigger)                       | 상세 로직(Logic)                                                                                                                                                                                                                                                                                                                                                                     | 예외 처리(Exception)                                                                                                                                                                                                                 | 데이터(I/O)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------- | ------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MAP_001_F01 | 지도 초기화         | 화면 진입 시 자동 실행              | 1. Geolocation API로 현재 위치 요청<br>2. `navigator.geolocation.getCurrentPosition()` 호출<br>3. 위치 권한 획득 시 `{ lat, lng }` 저장<br>4. Google Maps API 초기화:<br> - `new google.maps.Map(element, options)`<br> - 중심: 현재 위치<br> - 줌 레벨: 15<br>5. 현재 위치에 파란색 마커 표시                                                                                       | **위치 권한 거부**: Toast "위치 권한이 필요합니다" + 서울시청 좌표로 기본 설정<br>**GPS 오류**: Toast "위치를 가져올 수 없습니다" + 기본 위치 사용<br>**지도 로딩 실패**: Skeleton 맵 표시 + "지도를 불러올 수 없습니다" 에러 메시지 | **Output**:<br>`typescript<br>interface Location {<br>  lat: number;<br>  lng: number;<br>}<br>// 기본 좌표 (서울시청)<br>defaultLocation = {<br>  lat: 37.5665,<br>  lng: 126.9780<br>}<br>`                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| MAP_001_F02 | 주변 바 목록 조회   | 지도 로드 완료 시 자동              | 1. 현재 지도 중심 좌표를 기준으로 API 호출<br>2. `GET /api/bars/nearby?lat={lat}&lng={lng}&radius={radius}` 호출<br> - radius: 2000m (2km 반경)<br>3. 응답 받은 바 목록을 `bars` state에 저장<br>4. 각 바 위치에 빨간색 마커 표시<br>5. 마커 클릭 시 해당 바 정보 미리보기 (InfoWindow)                                                                                              | **Loading**: 지도 우측 하단에 작은 Spinner<br>**바 0개**: 지도 중앙에 "주변에 바가 없습니다" 메시지 Overlay<br>**API Error**: Toast "바 목록을 불러올 수 없습니다"                                                                   | **Input**: `{ lat: number, lng: number, radius: number }`<br>**Output**:<br>`typescript<br>interface Bar {<br>  id: string;<br>  name: string;<br>  address: string;<br>  latitude: number;<br>  longitude: number;<br>  distance: number; // 미터<br>  specialties: string[]; // ["Whiskey", "Cocktails"]<br>  rating: number;<br>  priceRange: number; // 1-4<br>}<br>`                                                                                                                                                                                                                                                                 |
| MAP_001_F03 | 바 목록 (리스트뷰)  | 화면 하단 Sheet 자동 표시           | 1. 지도 하단에 Draggable Sheet 렌더링<br>2. Sheet 내부에 바 목록을 카드 형태로 표시<br>3. 각 바 카드 구성:<br> - 바 이름<br> - 주소<br> - 거리 (예: "350m")<br> - 전문 주류 Badge (예: "위스키", "칵테일")<br> - 평점 별 표시<br> - 가격대 (₩₩₩)<br>4. 정렬: 거리순 (가까운 순)<br>5. 카드 클릭 시 지도 중심을 해당 바로 이동 + 마커 강조                                            | **Empty State**: "주변에 바가 없습니다" + "지도를 이동해서 검색해보세요" 안내<br>**Sheet 드래그**: 3단계 높이 (최소 → 중간 → 최대)                                                                                                   | **Display**:<br>`typescript<br>// 거리 포맷<br>distance < 1000: "{distance}m"<br>distance >= 1000: "{distance/1000}km"<br><br>// 가격대 표시<br>1: "₩"<br>2: "₩₩"<br>3: "₩₩₩"<br>4: "₩₩₩₩"<br>`                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| MAP_001_F04 | 바 상세 정보 조회   | 바 카드 또는 마커 클릭              | 1. 바 카드 또는 지도 마커 클릭<br>2. `GET /api/bars/{barId}` 호출하여 상세 정보 로드<br>3. Full Screen Dialog 렌더링<br>4. **주요 정보 표시**:<br> - 바 이름, 주소, 전화번호<br> - **보유 주류 목록** (Whiskey, Soju, Beer 등)<br> - 영업 시간 (JSON 파싱)<br> - 이미지 갤러리 (최대 5장)<br> - 평점 및 리뷰 수<br>5. "길찾기" 버튼 (Google Maps 앱 연동)<br>6. "즐겨찾기" 토글 버튼 | **Loading**: Dialog 내부 Skeleton<br>**API Error**: Toast "바 정보를 불러올 수 없습니다" + Dialog 닫기<br>**보유 주류 정보 없음**: "보유 주류 정보가 없습니다" 안내                                                                  | **Input**: `barId` (string)<br>**Output**:<br>`typescript<br>interface BarDetail {<br>  id: string;<br>  name: string;<br>  description: string;<br>  address: string;<br>  phone: string;<br>  website?: string;<br>  latitude: number;<br>  longitude: number;<br>  images: string[];<br>  openingHours: {<br>    mon: string; // "18:00-02:00"<br>    tue: string;<br>    wed: string;<br>    thu: string;<br>    fri: string;<br>    sat: string;<br>    sun: string;<br>  };<br>  specialties: string[]; // ✅ 보유 주류<br>  priceRange: number;<br>  rating: number;<br>  reviewCount: number;<br>  isFavorite: boolean;<br>}<br>` |
| MAP_001_F05 | 보유 주류 필터      | 화면 상단 Chip 그룹                 | 1. 지도 상단에 주류 카테고리 Chip 렌더링<br>2. Chip 옵션: [전체, Whiskey, Cocktails, Beer, Wine, Soju]<br>3. Chip 클릭 시 `selectedSpecialty` state 업데이트<br>4. 선택된 주류를 보유한 바만 필터링<br>5. 지도 마커 및 리스트뷰 실시간 업데이트<br>6. "전체" 선택 시 필터 해제                                                                                                       | **필터링 결과 0개**: "해당 주류를 보유한 바가 없습니다" Empty State                                                                                                                                                                  | **State**: `selectedSpecialty: "all" \| "Whiskey" \| "Cocktails" \| "Beer" \| "Wine" \| "Soju"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| MAP_001_F06 | 길찾기 (네비게이션) | 상세 Dialog 내부 "길찾기" 버튼 클릭 | 1. "길찾기" 버튼 클릭<br>2. 현재 위치와 바 위치를 Deep Link로 전달<br>3. Google Maps 앱 실행:<br> - `https://www.google.com/maps/dir/?api=1&destination={lat},{lng}`<br>4. 앱이 없으면 웹 브라우저에서 Google Maps 웹 버전 오픈                                                                                                                                                      | **위치 권한 없음**: "위치 권한이 필요합니다" Toast<br>**Google Maps 앱 없음**: 웹 브라우저로 자동 전환                                                                                                                               | **Output**: Deep Link URL 생성                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| MAP_001_F07 | 즐겨찾기 토글       | 상세 Dialog 내부 하트 버튼 클릭     | 1. 하트 아이콘 버튼 클릭<br>2. `isFavorite` state 토글<br>3. 추가 시: `POST /api/bars/{barId}/favorite` 호출<br>4. 제거 시: `DELETE /api/bars/{barId}/favorite` 호출<br>5. 성공 시 하트 아이콘 색상 변경 (회색 ↔ 빨강)<br>6. Toast "즐겨찾기에 추가/제거되었습니다"                                                                                                                 | **API Error**: Toast "즐겨찾기 실패" + 이전 상태로 복원<br>**401 Unauthorized**: "로그인이 필요합니다" Toast                                                                                                                         | **Input**: `barId` (string)<br>**Output**: `{ success: boolean, isFavorite: boolean }`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| MAP_001_F08 | 지도 이동 시 재검색 | 지도 드래그 완료 시                 | 1. 사용자가 지도를 드래그하여 이동<br>2. `onDragEnd` 이벤트 발생<br>3. 새로운 중심 좌표 획득<br>4. "이 지역 재검색" 플로팅 버튼 표시 (지도 상단)<br>5. 버튼 클릭 시 새 중심 좌표로 `MAP_001_F02` 재실행<br>6. 마커 및 리스트 업데이트                                                                                                                                                | **재검색 결과 0개**: "이 지역에는 바가 없습니다" Empty State                                                                                                                                                                         | **Trigger**: "이 지역 재검색" 버튼 클릭                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |

---

## 4. 칵테일 레시피 (Cocktail Recipes) - RECIPE_SCREEN ⭐

### 4.1 화면 개요

- **화면 ID**: `RECIPE_001`
- **경로**: `/recipes`
- **컴포넌트**: `CocktailRecipesScreen.tsx`
- **주요 기능**: 내 술장 기반 레시피 추천, 레시피 상세, 만들기 가이드
- **핵심 로직**: 보유한 술로 만들 수 있는 레시피 우선 정렬

---

### 4.2 기능 명세 테이블

| 화면ID         | 기능명                   | 구분(Trigger)                   | 상세 로직(Logic)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 예외 처리(Exception)                                                                                                                                                  | 데이터(I/O)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------------- | ------------------------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RECIPE_001_F01 | 추천 레시피 목록 조회    | 화면 진입 시 자동 실행          | 1. `GET /api/recipes/recommended` 호출<br>2. 쿼리 파라미터에 `userId` 포함 (서버가 내 술장 확인)<br>3. **서버 응답 (추천 알고리즘)**:<br> - 필수 재료를 **모두** 보유: `canMake = true` → "만들 수 있음" Badge (최우선 정렬)<br> - 필수 재료를 **일부만** 보유: `canMake = false` → "부분적으로 가능" Badge (2순위)<br> - 필수 재료를 **하나도 없음**: `canMake = false` → "추천 레시피" Badge (3순위)<br>4. **정렬 기준**:<br> - 1순위: `canMake === true` (보유 재료 100%)<br> - 2순위: `ownedIngredients / totalIngredients` 비율 높은 순<br> - 3순위: `rating` 평점 높은 순<br>5. 각 레시피 카드에 Badge 표시<br>6. Grid 형태로 렌더링 (2열) | **Loading**: Skeleton 카드 6개<br>**Empty**: "추천할 레시피가 없습니다" + "술을 추가해보세요" CTA<br>**API Error**: Toast "레시피를 불러올 수 없습니다" + 재시도 버튼 | **Input**: `userId` (자동)<br>**Output**:<br>`typescript<br>interface RecipeListItem {<br>  id: string;<br>  name: string;<br>  image: string;<br>  difficulty: "easy" \| "medium" \| "hard";<br>  ownedIngredients: number; // 보유 재료 수<br>  totalIngredients: number; // 총 필수 재료 수<br>  canMake: boolean; // ✅ ownedIngredients === totalIngredients<br>  badge: "만들 수 있음" \| "부분적으로 가능" \| "추천 레시피";<br>  rating: number;<br>  comments: number;<br>}<br>`                                                                     |
| RECIPE_001_F02 | 만들 수 있는 레시피 필터 | 화면 상단 토글 스위치           | 1. 화면 상단에 "만들 수 있는 레시피만 보기" 토글 스위치 렌더링<br>2. 토글 ON: `canMake === true`인 레시피만 필터링<br>3. 토글 OFF: 전체 레시피 표시<br>4. 실시간 필터링 (API 재호출 없음, 프론트엔드 필터)<br>5. 필터링 결과 개수 표시 (예: "12개 레시피")                                                                                                                                                                                                                                                                                                                                                                                       | **필터 결과 0개**: "아직 만들 수 있는 레시피가 없어요" Empty State + "술을 더 추가해보세요" CTA                                                                       | **State**: `showOnlyMakeable: boolean`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| RECIPE_001_F03 | 레시피 상세 보기         | 레시피 카드 클릭                | 1. 레시피 카드 클릭 시 Full Screen 화면으로 전환<br>2. `GET /api/recipes/{recipeId}?userId={userId}` 호출<br>3. 서버가 각 재료의 `owned` 여부를 체크하여 응답<br>4. **상세 정보 표시**:<br> - 레시피 이미지 (상단 배너)<br> - 이름, 난이도 Badge<br> - **재료 목록** (✅ 보유 / ❌ 미보유 표시)<br> - **제조 단계** (Step 1, 2, 3...)<br> - 팁/주의사항<br> - 평점 및 댓글 수<br>5. "만들기 시작" 버튼 (하단 고정)                                                                                                                                                                                                                               | **Loading**: 전체 화면 Skeleton<br>**API Error**: Toast "레시피 정보를 불러올 수 없습니다" + 이전 화면 복귀<br>**404 Not Found**: "삭제된 레시피입니다" Toast         | **Input**: `recipeId` (string), `userId` (자동)<br>**Output**:<br>`typescript<br>interface RecipeDetail {<br>  id: string;<br>  name: string;<br>  description: string;<br>  image: string;<br>  difficulty: string;<br>  ingredients: {<br>    name: string;<br>    amount: string; // "60ml", "1개"<br>    owned: boolean; // ✅ 핵심<br>    isOptional: boolean;<br>  }[];<br>  steps: {<br>    stepNumber: number;<br>    instruction: string;<br>    image?: string;<br>  }[];<br>  tips?: string;<br>  rating: number;<br>  comments: number;<br>}<br>` |
| RECIPE_001_F04 | 재료 보유 여부 표시      | 레시피 상세 렌더링 시 자동      | 1. 각 재료 옆에 상태 아이콘 표시<br>2. **보유 재료 (owned: true)**:<br> - ✅ 녹색 체크 아이콘<br> - 재료명을 일반 텍스트로 표시<br>3. **미보유 재료 (owned: false)**:<br> - ❌ 회색 X 아이콘<br> - 재료명을 회색 텍스트로 표시<br>4. **선택 재료 (isOptional: true)**:<br> - "(선택)" Badge 추가<br>5. 보유 재료 개수 / 전체 재료 개수 표시 (예: "3/5")                                                                                                                                                                                                                                                                                          | 예외 없음 (Pure Frontend Rendering)                                                                                                                                   | **Display Logic**:<br>`typescript<br>const ownedCount = ingredients.filter(i => i.owned).length;<br>const totalCount = ingredients.filter(i => !i.isOptional).length;<br>// "3/5 재료 보유 중"<br>`                                                                                                                                                                                                                                                                                                                                                           |
| RECIPE_001_F05 | 제조 단계 가이드         | "만들기 시작" 버튼 클릭         | 1. "만들기 시작" 버튼 클릭<br>2. 제조 단계를 Step-by-Step으로 표시하는 Modal 렌더링<br>3. 현재 단계 강조 (큰 번호 + 진행바)<br>4. "다음" 버튼 클릭 시 다음 단계로 이동<br>5. "이전" 버튼으로 이전 단계 복귀 가능<br>6. 마지막 단계에서 "완료" 버튼<br>7. 완료 시 "축하합니다! 🎉" 메시지 + 홈으로 복귀                                                                                                                                                                                                                                                                                                                                           | **첫 단계에서 "이전" 클릭**: 버튼 Disabled<br>**중간에 Modal 닫기**: "제조를 중단하시겠습니까?" 확인 Dialog                                                           | **State**:<br>`typescript<br>interface StepGuideState {<br>  currentStep: number; // 1-based<br>  totalSteps: number;<br>  isComplete: boolean;<br>}<br>`                                                                                                                                                                                                                                                                                                                                                                                                     |
| RECIPE_001_F06 | 난이도별 필터            | 화면 상단 Chip 그룹             | 1. 화면 상단에 난이도 Chip 렌더링: [전체, 쉬움, 보통, 어려움]<br>2. Chip 클릭 시 `selectedDifficulty` state 업데이트<br>3. 선택된 난이도의 레시피만 필터링<br>4. 프론트엔드 필터링 (API 재호출 없음)<br>5. 필터링 결과 개수 표시                                                                                                                                                                                                                                                                                                                                                                                                                 | **필터 결과 0개**: "해당 난이도의 레시피가 없습니다" Empty State                                                                                                      | **State**: `selectedDifficulty: "all" \| "easy" \| "medium" \| "hard"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| RECIPE_001_F07 | 즐겨찾기 토글            | 레시피 상세 화면 하트 버튼 클릭 | 1. 상세 화면 우측 상단 하트 아이콘 버튼<br>2. `isFavorite` state 토글<br>3. 추가 시: `POST /api/recipes/{recipeId}/favorite` 호출<br>4. 제거 시: `DELETE /api/recipes/{recipeId}/favorite` 호출<br>5. 성공 시 하트 아이콘 색상 변경 (회색 ↔ 빨강)<br>6. Toast "즐겨찾기에 추가/제거되었습니다"                                                                                                                                                                                                                                                                                                                                                  | **API Error**: Toast "즐겨찾기 실패" + 이전 상태로 복원<br>**401 Unauthorized**: "로그인이 필요합니다" Toast                                                          | **Input**: `recipeId` (string)<br>**Output**: `{ success: boolean, isFavorite: boolean }`                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| RECIPE_001_F08 | 부족한 재료 확인         | 레시피 상세 화면 버튼 클릭      | 1. 재료 목록 하단에 "부족한 재료 보기" 버튼 렌더링<br>2. 버튼 클릭 시 미보유 재료 목록을 Dialog로 표시<br>3. 각 재료 옆에 "검색" 버튼<br>4. "검색" 클릭 시 검색 화면으로 이동 (해당 재료명으로 자동 검색)<br>5. "모두 검색" 버튼으로 미보유 재료를 한 번에 검색 가능                                                                                                                                                                                                                                                                                                                                                                             | **부족한 재료 없음**: 버튼 숨김 + "모든 재료를 보유하고 있습니다 ✅" 메시지                                                                                           | **Output**:<br>`typescript<br>interface MissingIngredient {<br>  name: string;<br>  amount: string;<br>}<br>// 검색 화면으로 전달<br>const searchQuery = missingIngredients.map(i => i.name).join(" ");<br>`                                                                                                                                                                                                                                                                                                                                                  |

---

## 5. 설정/로그인 (Settings/Auth) - SETTINGS_SCREEN

### 5.1 화면 개요

- **화면 ID**: `SETTINGS_001`, `AUTH_001`
- **경로**: `/settings`, `/login`
- **컴포넌트**: `SettingsScreen.tsx`, `OnboardingScreen.tsx`
- **주요 기능**: 사용자 설정, 로그인/회원가입, 테마/언어 전환

---

### 5.2 기능 명세 테이블

| 화면ID           | 기능명                  | 구분(Trigger)                      | 상세 로직(Logic)                                                                                                                                                                                             | 예외 처리(Exception)                                                                                                                                              | 데이터(I/O)                                                                                                                                                                         |
| ---------------- | ----------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AUTH_001_F01     | 이메일 로그인           | 로그인 화면 "로그인" 버튼 클릭     | 1. 이메일, 비밀번호 Input<br>2. Validation: 이메일 형식, 비밀번호 8자 이상<br>3. `POST /api/auth/login` 호출<br>4. 성공 시 JWT 토큰을 로컬스토리지에 저장<br>5. 홈 화면으로 리다이렉트                       | **Validation 실패**: Input 하단 에러 메시지<br>**401 Unauthorized**: "이메일 또는 비밀번호가 틀렸습니다" Toast<br>**API Error**: "로그인 실패. 다시 시도해주세요" | **Input**:<br>`typescript<br>interface LoginRequest {<br>  email: string;<br>  password: string;<br>}<br>`<br>**Output**: `{ token: string, user: User }`                           |
| AUTH_001_F02     | 회원가입                | 회원가입 화면 "가입하기" 버튼 클릭 | 1. 이메일, 비밀번호, 비밀번호 확인 Input<br>2. Validation:<br> - 이메일 형식<br> - 비밀번호 8자 이상<br> - 비밀번호 일치<br>3. `POST /api/auth/register` 호출<br>4. 성공 시 자동 로그인 + 홈 화면 리다이렉트 | **이메일 중복**: "이미 사용 중인 이메일입니다" Toast<br>**Validation 실패**: Input 하단 에러 메시지<br>**API Error**: "회원가입 실패. 다시 시도해주세요"          | **Input**:<br>`typescript<br>interface RegisterRequest {<br>  email: string;<br>  password: string;<br>  username: string;<br>}<br>`<br>**Output**: `{ token: string, user: User }` |
| SETTINGS_001_F01 | 테마 전환 (Light/Dark)  | 설정 화면 토글 스위치              | 1. 설정 화면에서 "테마" 항목 렌더링<br>2. 토글 스위치 조작 시 `theme` state 변경<br>3. `ThemeProvider` context 업데이트<br>4. 전체 앱 색상 즉시 반영<br>5. 로컬스토리지에 `theme` 저장                       | 예외 없음 (Pure Frontend State)                                                                                                                                   | **State**: `theme: "light" \| "dark"`<br>**LocalStorage**: `localStorage.setItem("theme", theme)`                                                                                   |
| SETTINGS_001_F02 | 언어 전환 (한국어/영어) | 설정 화면 Select                   | 1. 설정 화면에서 "언어" 항목 렌더링<br>2. Select 변경 시 `language` state 변경<br>3. `LanguageProvider` context 업데이트<br>4. 모든 텍스트 즉시 번역<br>5. 로컬스토리지에 `language` 저장                    | 예외 없음 (Pure Frontend State)                                                                                                                                   | **State**: `language: "ko" \| "en"`<br>**LocalStorage**: `localStorage.setItem("language", language)`                                                                               |
| SETTINGS_001_F03 | 로그아웃                | 설정 화면 "로그아웃" 버튼 클릭     | 1. "로그아웃" 버튼 클릭<br>2. "정말 로그아웃하시겠습니까?" AlertDialog<br>3. 확인 시 로컬스토리지에서 토큰 삭제<br>4. 모든 state 초기화<br>5. 로그인 화면으로 리다이렉트                                     | 예외 없음                                                                                                                                                         | **Action**: `localStorage.removeItem("token")`<br>**Redirect**: `/login`                                                                                                            |
| SETTINGS_001_F04 | 프로필 수정             | 설정 화면 "프로필 편집" 버튼 클릭  | 1. Dialog로 프로필 수정 폼 렌더링<br>2. 표시명, 프로필 이미지 수정 가능<br>3. `PUT /api/users/profile` 호출<br>4. 성공 시 Toast "프로필이 수정되었습니다"                                                    | **Validation 실패**: "표시명을 2글자 이상 입력해주세요"<br>**API Error**: Toast "프로필 수정 실패"                                                                | **Input**:<br>`typescript<br>interface UpdateProfileRequest {<br>  displayName: string;<br>  avatarUrl?: string;<br>}<br>`<br>**Output**: `{ success: boolean }`                    |

---

## 📦 Phase 2: 추후 도입 기능 (요약)

### AI 블렌딩 랩 (AI Blending Lab)

- **우선순위**: 낮음
- **이유**: ML 모델 학습 및 데이터 부족
- **도입 시기**: Phase 1 안정화 후 (3-6개월 후)
- **핵심 기능**:
  - 곡물 배합 시뮬레이션
  - 숙성 공정 설정
  - AI 예측 결과 (색상, 향미 프로필, ABV)
- **필요 작업**:
  - 위스키 데이터셋 수집 (최소 500개)
  - TensorFlow.js 모델 학습
  - 서버 GPU 인프라

### 커뮤니티 (Community)

- **우선순위**: 중간
- **이유**: 초기 사용자 기반 확보 후 도입
- **도입 시기**: 사용자 1,000명 이상 확보 후
- **핵심 기능**:
  - 게시글 작성/수정/삭제 (CRUD)
  - 댓글 및 대댓글
  - 좋아요 (Toggle)
  - 이미지 업로드 (최대 5장)
  - 카테고리: 리뷰, 질문, 토론, 사진
- **필요 작업**:
  - 이미지 스토리지 (AWS S3 또는 Cloudinary)
  - 신고/차단 시스템
  - 관리자 대시보드

### 가격 추이 그래프 (Price History)

- **우선순위**: 중간
- **이유**: 가격 데이터 축적 필요 (최소 3개월)
- **도입 시기**: 크롤링 데이터 충분히 쌓인 후
- **핵심 기능**:
  - 제품별 가격 추이 Line Chart
  - 최저가/최고가 표시
  - 가격 알림 설정
- **필요 작업**:
  - 가격 크롤링 스크립트 (쿠팡, 마켓컬리 등)
  - Cron Job 자동화 (매일 1회)
  - Price History 테이블 데이터 축적

---

## 🔄 공통 데이터 규격 (Common Data Spec)

### API 응답 공통 형식

```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: {
    code: string;
    message: string;
  };
  timestamp: string; // ISO 8601
}
```

### 에러 코드 정의

| 에러 코드  | 의미               | 처리 방법                                          |
| ---------- | ------------------ | -------------------------------------------------- |
| `AUTH_001` | 인증 토큰 만료     | 자동 로그아웃 + 로그인 화면 리다이렉트             |
| `AUTH_002` | 토큰 없음          | 로그인 화면 리다이렉트                             |
| `VAL_001`  | Validation 실패    | Input 하단에 에러 메시지 표시                      |
| `NET_001`  | 네트워크 연결 끊김 | Toast "네트워크 연결을 확인해주세요" + 재시도 버튼 |
| `SRV_001`  | 서버 내부 오류     | Toast "일시적인 오류가 발생했습니다" + 재시도 버튼 |
| `RES_001`  | 리소스 없음 (404)  | Empty State 표시                                   |

### 로딩 상태 표준

- **전체 화면 로딩**: Full Screen Spinner (첫 진입 시)
- **부분 로딩**: Skeleton UI (카드, 리스트)
- **버튼 로딩**: 버튼 내부 Spinner + Disabled 상태
- **백그라운드 로딩**: 기존 데이터 유지 + 상단에 작은 Spinner

### 애니메이션 표준

| 동작        | 애니메이션           | Duration |
| ----------- | -------------------- | -------- |
| 카드 추가   | Slide-in from bottom | 500ms    |
| 카드 삭제   | Fade-out             | 300ms    |
| 탭 전환     | Fade-in              | 300ms    |
| Dialog 오픈 | Scale-up             | 200ms    |
| Dialog 닫기 | Scale-down           | 200ms    |
| Toast 표시  | Slide-in from top    | 300ms    |

---

## Phase 1 개발 우선순위

### Week 1-2: 기본 인프라

1. ✅ DB 스키마 구축 (PostgreSQL)
2. ✅ 인증 시스템 (JWT)
3. ✅ API 기본 구조 (FastAPI)

### Week 3-4: 내 술장 + 검색

1. ✅ 내 술장 CRUD
2. ✅ 검색 화면 (가격 정보 강조)
3. ✅ 필터링 기능

### Week 5-6: 바 지도 ⭐

1. ✅ Google Maps API 연동
2. ✅ 위치 기반 바 검색
3. ✅ 바 상세 정보 (보유 주류)

### Week 7-8: 칵테일 레시피 ⭐

1. ✅ 레시피 추천 알고리즘
2. ✅ 내 술장 기반 필터링
3. ✅ 제조 단계 가이드

### Week 9-10: 테스트 & 배포

1. ✅ 통합 테스트
2. ✅ 성능 최적화
3. ✅ 프로덕션 배포

---

## 📊 예상 API 목록 (Phase 1)

### 인증 (Auth)

- `POST /api/auth/login` - 로그인
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/refresh` - 토큰 갱신

### 내 술장 (Cabinet)

- `GET /api/cabinet/bottles` - 보유 술 목록
- `POST /api/cabinet/bottles` - 술 추가
- `DELETE /api/cabinet/bottles/{bottleId}` - 술 삭제

### 검색 (Search)

- `GET /api/products/search?q={query}` - 제품 검색
- `GET /api/products?category={category}&minPrice={min}&maxPrice={max}` - 필터링
- `GET /api/products/{productId}` - 제품 상세

### 바 지도 (Bar Map)

- `GET /api/bars/nearby?lat={lat}&lng={lng}&radius={radius}` - 주변 바 검색
- `GET /api/bars/{barId}` - 바 상세 정보
- `POST /api/bars/{barId}/favorite` - 즐겨찾기 추가
- `DELETE /api/bars/{barId}/favorite` - 즐겨찾기 제거

### 칵테일 레시피 (Recipes)

- `GET /api/recipes/recommended?userId={userId}` - 추천 레시피
- `GET /api/recipes/{recipeId}?userId={userId}` - 레시피 상세
- `POST /api/recipes/{recipeId}/favorite` - 즐겨찾기 추가
- `DELETE /api/recipes/{recipeId}/favorite` - 즐겨찾기 제거

### 사용자 (Users)

- `GET /api/users/profile` - 내 프로필
- `PUT /api/users/profile` - 프로필 수정

**총 API 수: 18개**

---

## ✅ 승인 및 피드백

### 변경 이력

| 버전 | 날짜       | 작성자 | 변경 내역                      |
| ---- | ---------- | ------ | ------------------------------ |
| v2.0 | 2025-12-14 | PM     | MVP 전략 반영 (Phase 1/2 분리) |
| v1.0 | 2024-12-13 | PM     | 초안 작성 (전체 기능)          |

**문서 종료** - Phase 1 상세 명세 완료 ✅
