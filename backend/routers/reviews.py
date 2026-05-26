from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User, Review
from auth_utils import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("")
def create_review(
    review: Review, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    try:
        review.user_id = current_user.user_id
        session.add(review)
        session.commit()
        session.refresh(review)
        
        return {"message": "리뷰 등록 완료!", "data": review}
    except Exception as e:
        raise HTTPException(status_code=500, detail="리뷰 등록 중 오류가 발생했습니다.")

@router.get("/lectures/{lecture_id}")
def get_lecture_reviews(lecture_id: int, session: Session = Depends(get_session)):
    statement = select(Review).where(Review.lecture_id == lecture_id)
    reviews = session.exec(statement).all()
    return reviews

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="관리자만 삭제할 수 있습니다.")
    
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="리뷰를 찾을 수 없습니다.")
    
    session.delete(review)
    session.commit()
    return {"message": "리뷰가 삭제되었습니다."}
