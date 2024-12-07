from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/accountant")
templates = Jinja2Templates(directory= "templates")
@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("accountant-page.html",
                                      {"request": request})