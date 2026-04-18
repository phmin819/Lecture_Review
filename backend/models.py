"""
[models.py]
역할: 데이터베이스 테이블 구조 정의 (ORMapping)
설명: SQLModel을 사용하여 파이썬 클래스와 DB 테이블을 1:1로 매칭
      User, Lecture, Review 간의 관계가 정의
"""

from typing import Optional
from sqlmodel import SQLModel, Field

# 1. 사용자 정보 테이블
class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str

# 2. 강의 정보 테이블
class Lecture(SQLModel, table=True):
    __tablename__ = "lectures"
    lecture_id: Optional[int] = Field(default=None, primary_key=True)
    lecture_name: str
    professor_name: str
    department: str

# 3. 강의 리뷰 테이블
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    review_id: Optional[int] = Field(default=None, primary_key=True)
    rating: int
    content: str
    
    # 외래키 설정: 어떤 유저가 어떤 강의에 썼는지 연결
    user_id: int = Field(foreign_key="users.user_id")    
    lecture_id: int = Field(foreign_key="lectures.lecture_id")