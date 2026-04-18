"""
[database.py]
역할: Neon PostgreSQL 데이터베이스와의 연결 및 세션 관리
설명: .env 파일의 접속 주소를 읽어와 SQLAlchemy 엔진을 생성하고, 
      각 API 요청 시 DB에 접근할 수 있는 세션을 제공
"""

import os
from sqlmodel import create_engine, Session
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

def get_session():
    with Session(engine) as session:
        yield session