from pydantic import BaseModel, EmailStr
from typing import Optional, Literal


Role = Literal["ADMIN", "AGENT"]

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Role = "AGENT"
    cognito_sub: Optional[str] = None


class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[Role] = None
    disabled: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role: Role
    disabled: bool

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    sub: str
    role: Optional[Role] = None