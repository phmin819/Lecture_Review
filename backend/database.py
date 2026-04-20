"""
[database.py]
역할: Neon PostgreSQL 데이터베이스 연결 및 세션 관리
설명: .env의 DATABASE_URL을 사용하여 SQLAlchemy 엔진을 생성하고,
     FastAPI의 Dependency Injection(Depends)을 통해 DB 세션을 제공함.
"""

import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def get_session():
    with Session(engine) as session:
        yield session

        print("DB:", os.getenv("DATABASE_URL"))