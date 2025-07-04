from pydantic import BaseModel, EmailStr


class Roles(BaseModel):
    role: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Roles


class UserUpdate(UserCreate):
    pass


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str
