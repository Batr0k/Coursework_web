from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.komendant import router as komendant_router
app = FastAPI()
app.include_router(komendant_router)
app.mount("/static", StaticFiles(directory="static"), name="static")