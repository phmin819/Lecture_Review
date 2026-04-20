"""
[auth_utils.py]
역할: 보안 및 인증 관련 핵심 유틸리티 로직
설명: bcrypt를 이용한 비밀번호 해싱/검증, JWT 토큰 생성 및 
     FastAPI Depends용 현재 로그인 사용자(get_current_user) 검증 로직 담당.
"""

import bcrypt
from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from database import get_session
from models import User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 1. 비밀번호 해싱 (bcrypt 직접 사용)
def hash_password(password: str) -> str:
    # 문자열을 바이트로 변환 후 솔트(Salt)를 추가하여 해싱
    pw_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw_bytes, salt)
    return hashed.decode('utf-8') # DB 저장을 위해 문자열로 변환

# 2. 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# 3. 토큰 생성 (기존과 동일)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 프론트엔드에서 헤더에 담아 보낼 토큰을 추출하는 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        # 토큰 복호화
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="인증 정보가 없습니다.")
    except Exception:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
    
    # DB에서 해당 이메일의 유저 확인
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user