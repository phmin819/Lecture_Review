from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import TimetableEntry, TimetableEntryCreate
from auth_utils import get_current_user

router = APIRouter(prefix="/timetable", tags=["timetable"])

@router.get("/me")
def get_my_timetable(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    entries = session.exec(
        select(TimetableEntry).where(TimetableEntry.user_id == current_user.user_id)
    ).all()
    return entries

@router.post("/me")
def add_timetable_entry(
    entry: TimetableEntryCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    new_entry = TimetableEntry(**entry.dict(), user_id=current_user.user_id)
    session.add(new_entry)
    session.commit()
    session.refresh(new_entry)
    return new_entry

@router.delete("/me/{entry_id}")
def delete_timetable_entry(
    entry_id: int,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    entry = session.get(TimetableEntry, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="항목을 찾을 수 없습니다.")
    if entry.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")
    session.delete(entry)
    session.commit()
    return {"ok": True}
