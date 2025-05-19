from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import main_router
from app.database import setup_database, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)
app.include_router(main_router)