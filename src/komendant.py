from fastapi import APIRouter, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi import Request
from src.schemas.komendant_schemas import OccupantPostDTO, OccupantGetDTO, FurniturePostDTO
router = APIRouter(prefix="/komendant")
templates = Jinja2Templates(directory= "templates")
from src.orm.komendant_orm import (select_all_occupant, add_occupant, get_occupant, update_occupant, select_rooms,
                                   select_furniture, select_free_rooms, select_furniture_by_id, update_furniture_description_and_room)

@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("komendant-page.html",
                                      {"request": request})


@router.get('/occupants')
async def get_residents():
    response = await select_all_occupant()
    return response
@router.put('/occupants/update/{id}')
async def put_occupant(id: int, occupant: OccupantPostDTO):
    await update_occupant(id, **occupant.dict())
@router.post('/occupants')
async def post_occupants(occupant: OccupantPostDTO):
    await add_occupant(**occupant.dict())
@router.get('/occupants/{id}')
async def get_occupant_by_id(id: int):
    return await get_occupant(id)
@router.get('/rooms')
async def get_rooms():
    return await select_rooms()
@router.get('/furniture')
async def get_furniture():
    return await select_furniture()
@router.get('/free_rooms')
async def get_free_rooms():
    return await select_free_rooms()
@router.get('/furniture/{id}')
async def get_furniture_by_id(id: int):
    return await select_furniture_by_id(id)
@router.put('/furniture/update/{id}')
async def put_furniture_description_and_room(id:int, furniture: FurniturePostDTO):
    await update_furniture_description_and_room(id, **furniture.dict())

