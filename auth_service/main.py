from fastapi import FastAPI
from app.api import auth
from app.models.base import Base
from app.database.session import engine


app = FastAPI()
app.include_router(auth.router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
