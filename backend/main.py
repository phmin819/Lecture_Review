"""
[main.py]
역할: FastAPI 애플리케이션 생성 및 API 엔드포인트(경로) 정의
설명: 프론트엔드(Vue.js)의 요청을 받아 DB 작업을 수행하고 결과를 반환
실행: uv run fastapi dev main.py
"""

from fastapi import FastAPI, Depends
from sqlmodel import select, Session
from database import get_session
from models import Lecture
from models import Review

app = FastAPI()

# [기능 1] 전체 강의 목록 조회
# 프론트엔드 메인 페이지에서 강의 리스트를 띄울 때 호출
@app.get("/lectures")
def read_lectures(session: Session = Depends(get_session)):    
    statement = select(Lecture)
    results = session.exec(statement).all()
    return results

# [기능 2] 신규 리뷰 등록
# 사용자가 리뷰 작성 후 '저장' 버튼을 눌렀을 때 호출
@app.post("/reviews")
def create_review(review: Review, session: Session = Depends(get_session)):
    session.add(review)         # DB 메모리에 추가
    session.commit()            # 실제 DB에 저장 확정
    session.refresh(review)     # 저장된 최신 데이터를 다시 불러오기
    return {"message": "리뷰가 성공적으로 등록되었습니다!", "data": review}