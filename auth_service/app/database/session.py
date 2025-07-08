from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


engine = create_async_engine(f"{settings.DATABASE_ENGINE}://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}" f"@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}")
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close()

