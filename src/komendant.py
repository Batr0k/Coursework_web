from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/komendant")
templates = Jinja2Templates(directory= "templates")
from src.orm.komendant_orm import select_all_occupant

@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("komendant-page.html",
                                      {"request": request})


@router.get('/occupants')
async def get_residents():
    response = await select_all_occupant()
    return response
@router.get('/occupants/{id}')
async def get_occupant_by_id(id: int):
    return {"message": "hi"}
