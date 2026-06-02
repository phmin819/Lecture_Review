from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import or_, and_
from pydantic import BaseModel
from database import get_session
from models import User, Friendship, TimetableEntry
from auth_utils import get_current_user

class FriendRequestBody(BaseModel):
    username: str

router = APIRouter(prefix="/friends", tags=["friends"])


def _friendship_status(session, my_id: int, other_id: int):
    """두 유저 사이의 친구 관계 row를 반환 (없으면 None)"""
    return session.exec(
        select(Friendship).where(
            or_(
                and_(Friendship.requester_id == my_id, Friendship.receiver_id == other_id),
                and_(Friendship.requester_id == other_id, Friendship.receiver_id == my_id),
            )
        )
    ).first()


# ── 유저 검색 ────────────────────────────────────────────
@router.get("/search")
def search_users(
    q: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not q.strip():
        return []
    users = session.exec(
        select(User).where(
            User.username.contains(q),
            User.user_id != current_user.user_id,
        ).limit(10)
    ).all()

    result = []
    for u in users:
        fs = _friendship_status(session, current_user.user_id, u.user_id)
        if fs:
            if fs.status == "accepted":
                status = "friends"
            elif fs.requester_id == current_user.user_id:
                status = "sent"
            else:
                status = "received"
        else:
            status = "none"
        result.append({
            "user_id": u.user_id,
            "username": u.username,
            "grade": u.grade,
            "friendship_status": status,
            "friendship_id": fs.id if fs else None,
        })
    return result


# ── 친구 요청 보내기 ─────────────────────────────────────
@router.post("/request")
def send_friend_request(
    body: FriendRequestBody,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    username = body.username.strip()
    target = session.exec(select(User).where(User.username == username)).first()
    if not target:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    if target.user_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="자신에게 요청할 수 없습니다.")

    existing = _friendship_status(session, current_user.user_id, target.user_id)
    if existing:
        raise HTTPException(status_code=400, detail="이미 친구이거나 요청이 존재합니다.")

    fs = Friendship(requester_id=current_user.user_id, receiver_id=target.user_id)
    session.add(fs)
    session.commit()
    session.refresh(fs)
    return {"id": fs.id, "status": fs.status}


# ── 받은 친구 요청 목록 ──────────────────────────────────
@router.get("/requests")
def get_received_requests(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    rows = session.exec(
        select(Friendship).where(
            Friendship.receiver_id == current_user.user_id,
            Friendship.status == "pending",
        )
    ).all()

    result = []
    for fs in rows:
        requester = session.get(User, fs.requester_id)
        result.append({
            "friendship_id": fs.id,
            "user_id": requester.user_id,
            "username": requester.username,
            "grade": requester.grade,
        })
    return result


# ── 친구 요청 수락 ───────────────────────────────────────
@router.put("/request/{friendship_id}/accept")
def accept_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    fs = session.get(Friendship, friendship_id)
    if not fs or fs.receiver_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="요청을 찾을 수 없습니다.")
    if fs.status != "pending":
        raise HTTPException(status_code=400, detail="이미 처리된 요청입니다.")
    fs.status = "accepted"
    session.add(fs)
    session.commit()
    return {"ok": True}


# ── 친구 요청 거절 / 요청 취소 ───────────────────────────
@router.delete("/request/{friendship_id}")
def decline_or_cancel_request(
    friendship_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    fs = session.get(Friendship, friendship_id)
    if not fs:
        raise HTTPException(status_code=404, detail="요청을 찾을 수 없습니다.")
    if fs.receiver_id != current_user.user_id and fs.requester_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    session.delete(fs)
    session.commit()
    return {"ok": True}


# ── 내 친구 목록 ─────────────────────────────────────────
@router.get("/me")
def get_my_friends(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    rows = session.exec(
        select(Friendship).where(
            or_(
                Friendship.requester_id == current_user.user_id,
                Friendship.receiver_id == current_user.user_id,
            ),
            Friendship.status == "accepted",
        )
    ).all()

    result = []
    for fs in rows:
        friend_id = fs.receiver_id if fs.requester_id == current_user.user_id else fs.requester_id
        friend = session.get(User, friend_id)
        result.append({
            "friendship_id": fs.id,
            "user_id": friend.user_id,
            "username": friend.username,
            "grade": friend.grade,
        })
    return result


# ── 친구 삭제 ────────────────────────────────────────────
@router.delete("/{user_id}")
def remove_friend(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    fs = _friendship_status(session, current_user.user_id, user_id)
    if not fs or fs.status != "accepted":
        raise HTTPException(status_code=404, detail="친구 관계를 찾을 수 없습니다.")
    session.delete(fs)
    session.commit()
    return {"ok": True}


# ── 친구 프로필 + 시간표 조회 ────────────────────────────
@router.get("/{user_id}/profile")
def get_friend_profile(
    user_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    fs = _friendship_status(session, current_user.user_id, user_id)
    if not fs or fs.status != "accepted":
        raise HTTPException(status_code=403, detail="친구만 프로필을 볼 수 있습니다.")

    friend = session.get(User, user_id)
    if not friend:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")

    timetable = session.exec(
        select(TimetableEntry).where(TimetableEntry.user_id == user_id)
    ).all()

    return {
        "user_id": friend.user_id,
        "username": friend.username,
        "grade": friend.grade,
        "timetable": [
            {
                "id": e.id,
                "day": e.day,
                "start_hour": e.start_hour,
                "end_hour": e.end_hour,
                "subject_name": e.subject_name,
                "color_bg": e.color_bg,
                "color_fg": e.color_fg,
            }
            for e in timetable
        ],
    }
