from fastapi import FastAPI
import uvicorn
from api import main_router
from contextlib import asynccontextmanager
from database_core import setup_database, engine
from api import main_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)
