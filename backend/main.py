"""
[main.py]
역할: FastAPI 애플리케이션 엔트리 포인트 및 API 엔드포인트 정의
설명: 500 에러 수정을 위해 데이터 변환 로직을 보강함.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate, Lecture, Review
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/signup")
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password) 
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "회원가입 성공!"}

@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}

# --- [수정된 부분] 500 에러 방지를 위해 dict 생성 로직을 안전하게 변경 ---
@app.get("/lectures")
def read_lectures(session: Session = Depends(get_session)):
    try:
        lectures = session.exec(select(Lecture)).all()
        result = []
        
        for lecture in lectures:
            statement = select(Review).where(Review.lecture_id == lecture.lecture_id)
            reviews = session.exec(statement).all()
            
            count = len(reviews)
            avg_rating = 0
            
            if count > 0:
                total_score = sum(r.rating for r in reviews)
                avg_rating = round(total_score / count, 1)
            
            # .dict() 대신 안전한 사전 생성 방식 사용
            lecture_item = {
                "lecture_id": lecture.lecture_id,
                "lecture_name": lecture.lecture_name,
                "professor_name": lecture.professor_name,
                "department": lecture.department,
                "avg_rating": avg_rating,
                "review_count": count
            }
            result.append(lecture_item)
            
        return result
    except Exception as e:
        # 서버 콘솔에 에러 로그 출력
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reviews")
def create_review(
    review: Review, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    review.user_id = current_user.user_id
    session.add(review)
    session.commit()
    session.refresh(review)
    return {"message": "리뷰 등록 완료!", "data": review}

@app.get("/lectures/{lecture_id}/reviews")
def get_lecture_reviews(lecture_id: int, session: Session = Depends(get_session)):
    statement = select(Review).where(Review.lecture_id == lecture_id)
    reviews = session.exec(statement).all()
    return reviews


//평균 점수 높은 순서대로 상위 5개 가져오기
@app.get("/lectures/trending")
def get_trending_lectures(session: Session = Depends(get_session)):
    # 1. 모든 강의 정보 가져오기
    statement = select(Lecture)
    lectures = session.exec(statement).all()
    
    trending = []
    for lecture in lectures:
        # 2. 해당 강의(lecture_id)의 리뷰들만 필터링
        rev_stmt = select(Review).where(Review.lecture_id == lecture.lecture_id)
        reviews = session.exec(rev_stmt).all()
        
        # 3. 평균 평점 계산
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        trending.append({
            "lecture_id": lecture.lecture_id,
            "lecture_name": lecture.lecture_name,
            "professor_name": lecture.professor_name,
            "department": lecture.department,
            "avg_rating": round(avg_rating, 1),
            "review_count": len(reviews)
        })
    
    # 4. 평점 높은 순으로 정렬 후 상위 5개 반환
    trending.sort(key=lambda x: x['avg_rating'], reverse=True)
    return trending[:5]


//프로필 기능
@app.get("/users/me")
def get_my_profile(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # 1. 내가(user_id) 쓴 모든 리뷰 가져오기
    statement = select(Review).where(Review.user_id == current_user.user_id)
    my_reviews = session.exec(statement).all()
    
    # 2. 프론트엔드에 전달할 프로필 패키지 구성
    return {
        "username": current_user.username,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "total_reviews": len(my_reviews),
        # 접근성 고려: 스크린 리더가 한 번에 읽기 좋은 요약 문구 추가
        "accessibility_summary": f"{current_user.username}님은 지금까지 총 {len(my_reviews)}개의 리뷰를 남기셨습니다."
    }