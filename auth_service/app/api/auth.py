from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.schemas.user import UserCreate, UserOut, Token
from app.services.auth import register_user, authenticate_user, get_current_user
from app.core.security import create_access_token
from app.database.session import get_db
from app.models.user import User


router = APIRouter(prefix="/api", tags=["Auth 🚪"])


@router.post("/register", response_model = UserOut)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(user_create, db)


@router.post("/login", response_model = Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(user.username, user.password, db)
    if not user:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail = "Неправильные данные")
    access_token = create_access_token(data = {"sub": user.username}, expires_delta = timedelta(minutes = 30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user", response_model = UserOut)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user
