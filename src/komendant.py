from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/komendant")
templates = Jinja2Templates(directory= "templates")


@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("komendant-page.html",
                                      {"request": request})


@router.get('/residents')
async def get_residents():
    resp = {"surname": "Дробот", "name": "Дима", "patronymic": "Николаевич", "Photo": " ",
             "phonenumber": "89254303103", "room": "819б", "check-in_date": "2023-08-31"}
    return JSONResponse(content=resp)
