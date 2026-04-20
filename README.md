# Lecture Review Project

Frontend : Vue.js 3
역할 : 사용자 UI 구현, 강의 목록 후기 작성 등 인터페이스 담당
선정이유 : Vue.js는 컴포넌트 기반 구조로 UI를 효율적으로 개발할 수 있으며 ,학습 난이도가 비교적 낮아 팀원들이 빠르게 적응할 수 있다 또한 API 연동이 용이하여 백엔드와의 통신에 적합하다.

Backend : FastAPI(Python)
역할 : Rest API 서버 구축, 로그인 강의 후기 데이터 처리
선정이유 : FastAPI는 Python 기반으로 간결한 코드로 빠르게 API를 개발할 수 있으며, 비동기 처리를 지원하여 성능이 우수하다.

DataBase : Neon (PostgreSQL)
역할 : 사용자, 강의, 후기 데이터 저장 및 관리
선정이유 : Neon은 PostgreSQL 기반의 클라우드 데이터베이스로 별도의 서버 구축 없이 빠르게 사용할 수 있으며 확장성과 관리 편의성이 뛰어나다.

시스템 구조 : Frontend (Vue.js) → Backend (FastAPI) → Database (Neon PostgreSQL)
