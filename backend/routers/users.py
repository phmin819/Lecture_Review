from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from database import get_session
from models import User, Review, ProfileUpdate
from auth_utils import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(func.count(Review.review_id)).where(Review.user_id == current_user.user_id)
    review_count = session.exec(statement).one()

    return {
        "username": current_user.username,
        "email": current_user.email,
        "phone_number": current_user.phone_number,
        "age": current_user.age,
        "gender": current_user.gender,
        "grade": current_user.grade, # 학년 추가
        "total_reviews": review_count,
        "accessibility_summary": f"{current_user.username}님은 지금까지 총 {review_count}개의 리뷰를 남기셨습니다."
    }

@router.put("/me")
def update_my_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    current_user.phone_number = profile_data.phone_number
    current_user.age = profile_data.age
    current_user.gender = profile_data.gender
    current_user.grade = profile_data.grade # 학년 추가
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    
    statement = select(func.count(Review.review_id)).where(Review.user_id == current_user.user_id)
    review_count = session.exec(statement).one()
    
    return {
        "message": "프로필 수정 완료!",
        "data": {
            "username": current_user.username,
            "email": current_user.email,
            "phone_number": current_user.phone_number,
            "age": current_user.age,
            "gender": current_user.gender,
            "grade": current_user.grade, # 학년 추가
            "total_reviews": review_count
        }
    }
