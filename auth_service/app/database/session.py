from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config.settings import DATABASE_ENGINE, DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_USER


engine = create_async_engine(f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}")
SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close()

