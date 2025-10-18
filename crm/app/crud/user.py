from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models import User, UserRole

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)

def create_user(db: Session, *, email: str, full_name: str | None, role: str, cognito_sub: str) -> User:
    user = User(
        email=email,
        full_name=full_name,
        role=UserRole(role),
        cognito_sub=cognito_sub,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, user: User, *, full_name: str | None = None, role: str | None = None, disabled: bool | None = None) -> User:
    if full_name is not None:
        user.full_name = full_name
    if role is not None:
        user.role = UserRole(role)
    if disabled is not None:
        user.disabled = disabled
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def disable_user(db: Session, user: User) -> User:
    user.disabled = True
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
