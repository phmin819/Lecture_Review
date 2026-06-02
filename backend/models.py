"""
[models.py]
역할: 데이터베이스 테이블 구조 정의 및 데이터 검증 (ORM)
설명: SQLModel을 사용하여 Neon DB의 users, lectures, reviews 테이블과 
     클래스를 매핑함. 인증을 위한 UserCreate 등 데이터 전송용 모델도 포함.
"""

from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- 1. User 관련 모델 (인증 로직 포함) ---
class UserBase(SQLModel):
    username: str
    email: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    __tablename__ = "users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(alias="password_hash")
    
    phone_number: Optional[str] = Field(default=None, nullable=True)
    age: Optional[int] = Field(default=None, nullable=True)
    gender: Optional[str] = Field(default=None, nullable=True)
    grade: Optional[int] = Field(default=None, nullable=True) # 학년 추가
    is_admin: bool = Field(default=False) # 관리자 여부 추가
    
    # 관계 설정: 유저가 작성한 리뷰들을 바로 참조 가능
    reviews: List["Review"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    password: str  # 회원가입 시 프론트에서 보내주는 생 비밀번호

class ProfileUpdate(SQLModel):
    phone_number: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    grade: Optional[int] = None # 학년 추가

# --- 2. Lecture 관련 모델 ---
class Lecture(SQLModel, table=True):
    __tablename__ = "lectures"
    lecture_id: Optional[int] = Field(default=None, primary_key=True)
    lecture_name: str
    professor_name: str
    department: str
    category: Optional[str] = Field(default=None, nullable=True)  # 학부
    class_time: Optional[str] = Field(default=None, nullable=True) # 강의 시간 추가

    # 관계 설정: 강의에 달린 리뷰들을 바로 참조 가능
    reviews: List["Review"] = Relationship(back_populates="lecture")

# --- 3. TimetableEntry 관련 모델 ---
class TimetableEntry(SQLModel, table=True):
    __tablename__ = "timetable_entries"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    day: str              # "월", "화", "수", "목", "금"
    start_hour: int       # 9 ~ 17
    end_hour: int         # 10 ~ 18
    subject_name: str
    color_bg: str = Field(default="#dbeafe")
    color_fg: str = Field(default="#1d4ed8")

class TimetableEntryCreate(SQLModel):
    day: str
    start_hour: int
    end_hour: int
    subject_name: str
    color_bg: str = "#dbeafe"
    color_fg: str = "#1d4ed8"

# --- 4. Friendship 관련 모델 ---
class Friendship(SQLModel, table=True):
    __tablename__ = "friendships"
    id: Optional[int] = Field(default=None, primary_key=True)
    requester_id: int = Field(foreign_key="users.user_id")
    receiver_id: int = Field(foreign_key="users.user_id")
    status: str = Field(default="pending")  # "pending" | "accepted"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# --- 5. Review 관련 모델 ---
class Review(SQLModel, table=True):
    __tablename__ = "reviews"
    review_id: Optional[int] = Field(default=None, primary_key=True)
    rating: int
    content: str
    
    # 외래키 (Neon DB의 실제 컬럼명과 일치해야 함)
    user_id: int = Field(foreign_key="users.user_id")
    lecture_id: int = Field(foreign_key="lectures.lecture_id")
    
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # 관계 설정: 리뷰 객체에서 바로 유저나 강의 정보를 조회 가능
    user: Optional[User] = Relationship(back_populates="reviews")
    lecture: Optional[Lecture] = Relationship(back_populates="reviews")