"""
[main.py]
역할: FastAPI 애플리케이션 엔트리 포인트 및 API 엔드포인트 정의
설명: 회원가입, 로그인(JWT), 강의 조회, 리뷰 등록 등의 API 경로를 설정하며
     CORS 설정 및 인증 미들웨어를 통합하여 프론트엔드와 통신함.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate, Lecture, Review
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

# 프론트엔드(Vue.js)와의 통신을 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 개발 중에는 모두 허용, 배포 시에는 프론트 주소만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [기능 1] 회원가입
@app.post("/auth/signup")
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    # 이미 존재하는 이메일인지 확인
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    # 비밀번호 해싱 후 저장
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password) 
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "회원가입 성공!"}

# [기능 2] 로그인 (JWT 발급)
@app.post("/auth/login")
def login(
    # 기존 user_data: UserCreate 대신 아래 폼 형식을 사용합니다.
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    # OAuth2 표준에 따라 form_data.username에는 이메일 값이 들어옵니다.
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    # 비밀번호 검증 (이미지상 컬럼명인 password_hash 사용)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    # 토큰 생성
    access_token = create_access_token(data={"sub": user.email, "user_id": user.user_id})
    
    # OAuth2 표준 리턴 형식 (이 형식을 지켜야 Swagger 자물쇠가 잠깁니다)
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

# [기능 3] 전체 강의 목록 조회 (기존 유지)
@app.get("/lectures")
def read_lectures(session: Session = Depends(get_session)):    
    return session.exec(select(Lecture)).all()



@app.post("/reviews")
def create_review(
    review: Review, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # 로그인 체크
):
    # 로그인한 유저의 ID를 리뷰의 user_id로 자동 설정
    review.user_id = current_user.user_id
    
    session.add(review)
    session.commit()
    session.refresh(review)
    return {"message": "리뷰 등록 완료!", "data": review}