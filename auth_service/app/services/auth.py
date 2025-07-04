from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.database.session import get_db
from app.core.config import settings


bearer_scheme = HTTPBearer()


async def register_user(user_create: UserCreate, db: AsyncSession):
    user = User(
        username = user_create.username,
        email = user_create.email,
        password = hash_password(user_create.password),
        role = user_create.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(username: str, email: str, password: str, role: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username) and select(User).where(User.email == email) and select(User).where(User.role == role))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        None
    return user


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail = "Недействительный токен")
    except JWTError:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail = "Недействительный токен")
    
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code = HTTP_401_UNAUTHORIZED, detail = "Пользователь не найден")
    return user
