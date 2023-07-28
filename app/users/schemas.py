from pydantic import BaseModel, EmailStr


class SUserAuth(BaseModel):
    email: EmailStr
    password: str


class SUserInfo(BaseModel):
    email: EmailStr
    id: int