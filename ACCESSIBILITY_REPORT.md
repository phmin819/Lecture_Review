# 웹 접근성 리포트

## 개요
- 생성일: 2026-04-28
- 대상: `frontend` 앱의 주요 페이지
  - 홈 페이지 (`HomeView.vue`)
  - 강의 상세 페이지 (`LectureDetailView.vue`)
  - 로그인 페이지 (`LoginView.vue`)
  - 회원가입 페이지 (`RegisterView.vue`, `SignupView.vue`)
- 점검 방법: 코드 리뷰 기반 KWCAG 검토, 로컬 앱 렌더링 시도
- 사용 가능한 자동화 도구: Browser MCP (`@browsermcp/mcp` npm 패키지 확인 완료, 버전 0.1.3)

## 점검 결과 요약
- 현재 앱은 기본적인 UI를 제공하지만, 웹 접근성 관점에서 다음과 같은 주요 개선이 필요합니다.
  1. 시멘틱 마크업 부족
  2. 폼 라벨 부재 및 폼 컨트롤 접근성 부족
  3. 키보드 네비게이션 불완전
  4. `aria` 속성 및 역할(role) 부족
  5. 한국어 콘텐츠에 맞지 않는 `lang` 속성

## KWCAG 기반 주요 발견사항

### 1. 지각 가능성 (Perceivable)
- `frontend/index.html`의 `<html lang="en">`가 한국어 콘텐츠에 부적절함. `lang="ko"`로 변경 필요.
- 로그인/회원가입 페이지의 입력 필드가 `placeholder`만 사용됨. `label`이 없어 스크린 리더 사용자가 필드 목적을 파악하기 어렵습니다.
- `lecture` 카드, 별점 입력 등 비표준 컨트롤에 명시적 레이블이 없음.
- 텍스트 대비 비율이 명시적으로 검증되지 않았으며, 연한 회색 텍스트는 WCAG AA 대비 불충분할 가능성이 큼.

### 2. 운영 가능성 (Operable)
- 강의 목록 항목이 `div` 요소에 `@click` 처리되어 있음. 키보드 포커스/Enter 입력/스크린 리더 접근성이 없음.
- LectureDetail 페이지의 별점 입력(`span` 요소 클릭)과 뒤로가기 요소가 키보드로 작동하지 않음.
- 로그인/회원가입이 `button @click` 형태로 구현되어 있지만 `<form>` 태그와 `type="submit"`이 없어 브라우저 기본 폼 동작이 활용되지 않음.
- 사용자 정의 인터랙티브 요소에 `tabindex`나 `role`이 없음.

### 3. 이해 가능성 (Understandable)
- 로그인/회원가입 페이지에 서로 동일한 수준의 `<h2>`가 반복돼 제목 구조가 불분명함.
- 클라이언트 유효성 검사 실패 시 시각적 알림은 있으나 `aria-live` 같은 접근성 피드백 영역이 없어 보조기기 사용자에게 전달되지 않음.
- 리뷰 섹션 및 평점 바의 의미가 시멘틱하게 설명되지 않음.

### 4. 견고성 (Robust)
- 커스텀 버튼/링크 기능에 ARIA 역할이 없는 경우, 보조기기가 해당 요소를 적절히 해석하지 못할 수 있음.
- 동적 컨텐츠 상태(로딩, 오류)의 접근성 전이가 충분히 정의되지 않음.

## 페이지별 상세 리스크

### 홈 페이지 (`HomeView.vue`)
- 검색 입력에 `<label>` 없음
- 강의 카드가 버튼/링크 대신 `div`로 구성됨
- 로딩 상태가 시맨틱하지 않음(텍스트만 표시)
- `cursor: pointer`는 충분하지 않음

### 강의 상세 페이지 (`LectureDetailView.vue`)
- 뒤로가기 텍스트가 버튼/링크로 처리되지 않음
- 별점 입력 UI가 `span`으로 구현돼 키보드 접근성 취약
- 리뷰 항목에 작성일, 사용자 정보가 있지만 시멘틱 `time`/`aria-label` 없음
- 평점바가 시각적 정보만 제공됨

### 로그인/회원가입 페이지 (`LoginView.vue`, `RegisterView.vue`, `SignupView.vue`)
- 입력 필드가 `label` 없이 `placeholder`만 사용됨
- 버튼과 링크 역할이 혼재됨 (`p`/`span` 요소에 클릭 이벤트)
- 폼 자체가 `<form>` 요소로 구성되어 있지 않아 접근성 폼 작동이 제한됨

## 개선 제안

### A. 시멘틱 HTML 및 폼 개선
- 모든 입력에 `<label for="...">` 추가
- 로그인/회원가입을 `<form>`으로 구성하고 `type="submit"`을 사용
- 강의 목록 항목은 `<a>` 또는 `<button>` 요소로 교체
- 뒤로가기/로그인 링크는 `<button>`/`<a>`로 변경

### B. 키보드 접근성 보강
- 터치/클릭 전용 `div`를 제거하고 포커스 가능한 요소로 대체
- 커스텀 컨트롤에 `tabindex="0"` 및 `@keyup.enter`/`@keyup.space` 핸들러 추가
- `:focus-visible` 스타일을 추가하여 키보드 포커스 식별성 확보

### C. ARIA 및 상태 메시지
- 사용자 알림에 `role="alert"` 또는 `aria-live="polite"` 적용
- 아이콘 기반 버튼에 `aria-label` 추가 (예: 뒤로가기, 별점 선택)
- `role="status"` 또는 `aria-busy`로 로딩 상태 표시

### D. 한국어 콘텐츠 및 메타
- `frontend/index.html`의 `<html lang="ko">` 변경
- `meta charset="UTF-8"`는 이미 있으므로 meta 항목은 유지
- `aria` 속성과 적절한 언어 설정으로 한국어 화면에 맞게 최적화

## Browser MCP 활용 제안

### 적절한 도구
- `Browser MCP`는 브라우저 자동 제어와 페이지 스냅샷 생성에 최적화된 MCP 도구입니다.
- 특히 VS Code 환경에서 로컬 개발 서버(`http://localhost:5173/`)를 자동화하고, 각 페이지를 순차적으로 탐색하면서 접근성 검사 스냅샷을 수집하는 데 적합합니다.

### 권장 워크플로
1. 브라우저에 Browser MCP 확장 설치
2. VS Code 워크스페이스에 MCP 서버 구성
3. 로컬 앱을 실행 (`npm run dev -- --host 127.0.0.1`)
4. Browser MCP를 통해:
   - 홈 페이지 접속
   - 강의 상세 페이지 접속
   - 로그인/회원가입 폼 순회
   - 접근성 스냅샷 및 콘솔 로그 수집

### 설치 및 실행
- `@browsermcp/mcp` 패키지는 npm에서 확인됨 (버전 0.1.3)
- 서버 실행 예:
  ```bash
  npx @browsermcp/mcp@latest
  ```
- VS Code 설정 예:
  ```json
  {
    "mcpServers": {
      "browsermcp": {
        "command": "npx",
        "args": ["@browsermcp/mcp@latest"]
      }
    }
  }
  ```

## 현 환경에서 발견된 제한사항
- 통합 브라우저 자동화 환경에서 `http://localhost:5173` 접근 시 실제 페이지 렌더링이 불완전했습니다.
- 따라서 이 리포트는 주로 코드 기반 KWCAG 리뷰와 현 앱 구조 분석을 기반으로 작성되었습니다.
- 이후 브라우저 확장 설치 후 Browser MCP로 실제 페이지를 재검사하는 것을 권장합니다.

## 다음 단계
1. 위 개선 사항을 반영한 UI/폼 수정
2. `lang="ko"` 및 `label`/`aria-*` 보강
3. 키보드 네비게이션과 포커스 스타일 추가
4. Browser MCP로 전체 경로 자동 검사
