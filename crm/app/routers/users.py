from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user, admin_required
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.crud.user import get_user_by_email, get_user_by_id, create_user, update_user, disable_user, delete_user

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("", response_model=UserOut)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db), _: any = Depends(admin_required)):
    if get_user_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already exists")
    user = create_user(
        db,
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        cognito_sub=payload.cognito_sub or "",
    )
    return user

@router.patch("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    current_role = current.get("custom:role") or current.get("role")
    current_sub = current.get("sub")

    # admin can update anyone, user can only update themselves
    if current_role != "ADMIN" and current_sub != user.cognito_sub:
        raise HTTPException(status_code=403, detail="Not allowed")

    updated = update_user(db, user, full_name=payload.full_name, role=payload.role, disabled=payload.disabled)
    return updated

@router.patch("/{user_id}/disable", response_model=UserOut)
def disable_user_endpoint(user_id: int, db: Session = Depends(get_db), _: any = Depends(admin_required)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return disable_user(db, user)

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), _: any = Depends(admin_required)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    return {"detail": "deleted"}

@router.get("/me", response_model=dict)
def get_my_profile(current = Depends(get_current_user)):
    return {
        "email": current.get("email"),
        "role": current.get("custom:role") or current.get("role"),
        "sub": current.get("sub")
    }
