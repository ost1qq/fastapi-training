from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.api import main_router
from app.database import setup_database
from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=4200)
