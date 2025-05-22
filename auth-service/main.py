from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
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
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
