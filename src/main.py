from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.komendant import router as komendant_router
from src.accountant import router as accountant_router
from src.director import router as director_router
app = FastAPI()
app.include_router(komendant_router)
app.include_router(accountant_router)
app.include_router(director_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})