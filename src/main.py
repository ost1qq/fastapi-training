from fastapi import FastAPI
import uvicorn
from src.api import main_router

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="127.0.0.1", port=4200, reload=True)
