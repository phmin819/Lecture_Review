from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from database import get_session
from models import Lecture, Review, User
from auth_utils import get_current_user
from typing import Optional

router = APIRouter(prefix="/lectures", tags=["lectures"])

@router.get("")
def read_lectures(search: Optional[str] = None, session: Session = Depends(get_session)):
    # 최적화: SQL Join 및 Aggregation을 사용하여 N+1 문제 해결
    # 평점 높은 순으로 정렬 추가
    statement = (
        select(
            Lecture.lecture_id,
            Lecture.lecture_name,
            Lecture.professor_name,
            Lecture.department,
            func.count(Review.review_id).label("review_count"),
            func.avg(Review.rating).label("avg_rating")
        )
        .outerjoin(Review, Review.lecture_id == Lecture.lecture_id)
        .group_by(Lecture.lecture_id)
        .order_by(func.avg(Review.rating).desc().nulls_last(), Lecture.lecture_name.asc())
    )
    
    if search:
        statement = statement.where(
            (Lecture.lecture_name.contains(search)) | 
            (Lecture.professor_name.contains(search))
        )
        
    results = session.exec(statement).all()
    
    return [
        {
            "lecture_id": r.lecture_id,
            "lecture_name": r.lecture_name,
            "professor_name": r.professor_name,
            "department": r.department,
            "review_count": r.review_count,
            "avg_rating": round(float(r.avg_rating), 1) if r.avg_rating else 0
        }
        for r in results
    ]

@router.get("/trending")
def get_trending_lectures(session: Session = Depends(get_session)):
    # 리뷰가 1개 이상이고 평점이 있는 강의만 필터링 (having 사용)
    statement = (
        select(
            Lecture.lecture_id,
            Lecture.lecture_name,
            Lecture.professor_name,
            Lecture.department,
            func.count(Review.review_id).label("review_count"),
            func.avg(Review.rating).label("avg_rating")
        )
        .join(Review, Review.lecture_id == Lecture.lecture_id) # inner join으로 리뷰 있는 것만
        .group_by(Lecture.lecture_id)
        .having(func.count(Review.review_id) > 0)
        .order_by(func.avg(Review.rating).desc())
        .limit(5)
    )
    
    results = session.exec(statement).all()
    
    return [
        {
            "lecture_id": r.lecture_id,
            "lecture_name": r.lecture_name,
            "professor_name": r.professor_name,
            "department": r.department,
            "review_count": r.review_count,
            "avg_rating": round(float(r.avg_rating), 1) if r.avg_rating else 0
        }
        for r in results
    ]

@router.get("/{lecture_id}/reviews")
def get_lecture_reviews(lecture_id: int, session: Session = Depends(get_session)):
    # 리뷰와 작성자 정보를 함께 가져옴
    statement = (
        select(Review, User.username)
        .join(User, Review.user_id == User.user_id)
        .where(Review.lecture_id == lecture_id)
        .order_by(Review.created_at.desc())
    )
    results = session.exec(statement).all()
    
    return [
        {
            "review_id": r[0].review_id,
            "rating": r[0].rating,
            "content": r[0].content,
            "created_at": r[0].created_at.isoformat(),
            "username": r[1]
        }
        for r in results
    ]

@router.get("/{lecture_id}")
def read_lecture_detail(lecture_id: int, session: Session = Depends(get_session)):
    statement = (
        select(
            Lecture.lecture_id,
            Lecture.lecture_name,
            Lecture.professor_name,
            Lecture.department,
            Lecture.class_time, # 추가
            func.count(Review.review_id).label("review_count"),
            func.avg(Review.rating).label("avg_rating")
        )
        .outerjoin(Review, Review.lecture_id == Lecture.lecture_id)
        .where(Lecture.lecture_id == lecture_id)
        .group_by(Lecture.lecture_id)
    )
    
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="강의를 찾을 수 없습니다.")
        
    return {
        "lecture_id": result.lecture_id,
        "lecture_name": result.lecture_name,
        "professor_name": result.professor_name,
        "department": result.department,
        "class_time": result.class_time, # 추가
        "review_count": result.review_count,
        "avg_rating": round(float(result.avg_rating), 1) if result.avg_rating else 0
    }

@router.put("/{lecture_id}")
def update_lecture(
    lecture_id: int,
    lecture_data: Lecture,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="관리자만 수정할 수 있습니다.")
    
    lecture = session.get(Lecture, lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="강의를 찾을 수 없습니다.")
    
    lecture.lecture_name = lecture_data.lecture_name
    lecture.professor_name = lecture_data.professor_name
    lecture.department = lecture_data.department
    lecture.class_time = lecture_data.class_time # 추가
    
    session.add(lecture)
    session.commit()
    session.refresh(lecture)
    return lecture
