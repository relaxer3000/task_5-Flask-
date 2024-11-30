from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy import func

from database.connection import get_session
from models.user import User, UserEmailUpdate


user_router = APIRouter(tags=["User"])


@user_router.get("/")
async def get_users(session: Session = Depends(get_session)) -> Sequence[User]:
    users = session.exec(select(User).order_by(User.create_at)).all()
    return users


@user_router.get("/filter")
async def get_filter_users(string_filter: str, session: Session = Depends(get_session)) -> Sequence[User]:
    string_filter_db = f'%{string_filter}%'
    users = session.exec(select(User).where(func.lower(User.username).like(string_filter_db))).all()
    return users


@user_router.get("/pagination")
async def get_pagination_users(page: int, page_size: int, session: Session = Depends(get_session)) -> Sequence[User]:
    offset = (page - 1) * page_size
    users = session.exec(select(User).offset(offset).limit(page_size)).all()
    return users


@user_router.post("/")
async def create_user(user: User, session: Session = Depends(get_session)) -> User:
    user_db = User(**user.model_dump(exclude={"id", "create_at"}))
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@user_router.patch("/{user_id}")
async def update_user(user_id: int, user: UserEmailUpdate, session: Session = Depends(get_session)) -> User:
    user_db = session.exec(select(User).where(User.id == user_id)).first()
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID not found",
        )
    user_db.email = user.email

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@user_router.delete("/{user_id")
async def delete_user(user_id: int, session: Session = Depends(get_session)) -> bool:
    user_db = session.exec(select(User).where(User.id == user_id)).first()
    try:
        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with supplied ID not found",
            )
    except HTTPException:
        return False

    session.delete(user_db)
    session.commit()

    return True
