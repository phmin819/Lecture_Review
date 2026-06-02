# 명지전문대 강의 후기 플랫폼

명지전문대학교 학생들이 수강한 강의에 대한 후기를 작성하고 공유할 수 있는 웹 서비스입니다.

---

## 주요 기능

| 기능 | 설명 |
|------|------|
| 강의 목록 / 검색 | 강의명·교수명으로 검색, 평점순 정렬 |
| 강의 상세 / 후기 | 별점(1~5) + 텍스트 후기 작성·조회 |
| 인기 강의 | 평점 상위 5개 강의 메인 화면 노출 |
| 회원가입 / 로그인 | JWT 기반 토큰 인증 |
| 마이 페이지 | 학년·성별·나이·연락처 정보 수정 |
| 나의 시간표 | 드래그로 시간 범위 선택 → 수업명·색상 설정, DB 저장 |

---

## 기술 스택

### Frontend
- **Vue.js 3** — 컴포넌트 기반 UI, Vue Router 페이지 전환
- **Axios** — REST API 통신

### Backend
- **FastAPI** — API 서버, Swagger UI 자동 생성
- **SQLModel** — ORM (데이터 모델 + 스키마 일원화)
- **JWT (python-jose)** — 토큰 기반 인증
- **bcrypt (passlib)** — 비밀번호 단방향 해시

### Database
- **Neon (PostgreSQL)** — 클라우드 PostgreSQL, 팀 공용 DB

### 도구
- **uv** — Python 패키지 / 가상환경 관리
- **Vite** — 프론트엔드 빌드 도구

---

## 프로젝트 구조

```
Lecture_Review/
├── backend/
│   ├── main.py              # FastAPI 앱 진입점, CORS 설정
│   ├── models.py            # DB 테이블 모델 (User, Lecture, Review, TimetableEntry)
│   ├── database.py          # DB 연결 설정
│   ├── auth_utils.py        # JWT 토큰 발급·검증
│   └── routers/
│       ├── auth.py          # POST /auth/signup, /auth/login
│       ├── lectures.py      # GET /lectures, /lectures/{id}, /lectures/trending
│       ├── reviews.py       # POST /lectures/{id}/reviews
│       ├── users.py         # GET/PUT /users/me
│       └── timetable.py     # GET/POST/DELETE /timetable/me
│
└── frontend/
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── components/
        │   └── TimetableGrid.vue   # 시간표 드래그 컴포넌트
        └── views/
            ├── HomeView.vue        # 메인 (강의 목록 + 인기 강의)
            ├── LoginView.vue
            ├── SignupView.vue
            ├── LectureDetailView.vue
            └── ProfileView.vue     # 마이페이지 (시간표 포함)
```

---

## API 엔드포인트 요약

| Method | Path | 설명 | 인증 |
|--------|------|------|------|
| POST | `/auth/signup` | 회원가입 | - |
| POST | `/auth/login` | 로그인 (JWT 발급) | - |
| GET | `/lectures` | 강의 목록 (검색 지원) | - |
| GET | `/lectures/trending` | 인기 강의 Top 5 | - |
| GET | `/lectures/{id}` | 강의 상세 | - |
| GET | `/lectures/{id}/reviews` | 강의 후기 목록 | - |
| POST | `/lectures/{id}/reviews` | 후기 작성 | ✅ |
| PUT | `/lectures/{id}` | 강의 수정 (관리자) | ✅ |
| GET | `/users/me` | 내 프로필 조회 | ✅ |
| PUT | `/users/me` | 내 프로필 수정 | ✅ |
| GET | `/timetable/me` | 내 시간표 조회 | ✅ |
| POST | `/timetable/me` | 시간표 항목 추가 | ✅ |
| DELETE | `/timetable/me/{id}` | 시간표 항목 삭제 | ✅ |

---

## 실행 방법

### 백엔드

```bash
cd backend
uv sync           # 의존성 설치
uv run uvicorn main:app --reload
# → http://127.0.0.1:8000
# → http://127.0.0.1:8000/docs  (Swagger UI)
```

### 프론트엔드

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## 시간표 기능 사용법

1. 로그인 후 **마이 페이지** 이동
2. 시간표 섹션에서 **✏️ 편집 모드** 버튼 클릭
3. 원하는 시간 칸을 **마우스로 드래그**하여 범위 선택
4. 팝업에서 **수업명 입력** + **색상 선택** 후 저장
5. 수업 블록에 마우스를 올리면 **× 버튼**으로 삭제 가능
6. 데이터는 DB에 저장되어 재접속 시에도 유지됨
