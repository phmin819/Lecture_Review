from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from database import get_session
from models import User, UserCreate
from auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    clean_email = user_data.email.strip()
    existing_user = session.exec(select(User).where(User.email == clean_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    new_user = User(
        username=user_data.username,
        email=clean_email,
        password_hash=hash_password(user_data.password) 
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "회원가입 성공!"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    print(f"[DEBUG] Login attempt - Username: {form_data.username}")
    
    # 특수 관리자 계정 처리
    if form_data.username == "rhksflwk" and form_data.password == "rhksflwk":
        print("[DEBUG] Admin credentials matched")
        # DB에 관리자 계정이 없으면 자동 생성 (혹은 기존 정보 확인)
        admin_user = session.exec(select(User).where(User.email == "rhksflwk")).first()
        if not admin_user:
            print("[DEBUG] Admin user not found in DB, creating...")
            admin_user = User(
                username="관리자",
                email="rhksflwk",
                password_hash=hash_password("rhksflwk"),
                is_admin=True
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)
            print(f"[DEBUG] Admin user created with ID: {admin_user.user_id}")
        
        access_token = create_access_token(data={"sub": admin_user.email, "user_id": admin_user.user_id, "is_admin": True})
        return {"access_token": access_token, "token_type": "bearer", "is_admin": True}

    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )
    
    access_token = create_access_token(data={"sub": user.email, "user_id": user.user_id, "is_admin": user.is_admin})
    return {"access_token": access_token, "token_type": "bearer", "is_admin": user.is_admin}
