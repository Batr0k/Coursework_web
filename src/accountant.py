from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from datetime import date
from src.schemas.accountant_shemas import CostPerMonthPostDTO, FurniturePostDTO
from src.orm.accountant_orm import (select_payments, select_cost_per_month, select_occupants, insert_payment,
                                    insert_cost_per_month, select_furniture, insert_furniture, delete_furniture)
router = APIRouter(prefix="/accountant")
templates = Jinja2Templates(directory= "templates")
@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("accountant-page.html",
                                      {"request": request})
@router.get('/payments')
async def get_payments():
    return await select_payments()
@router.get('/cost_per_month')
async def get_cost_per_month():
    return await select_cost_per_month()
@router.get('/occupants')
async def get_occupants():
    return await select_occupants()
@router.post('/insert_payment')
async def insert__payment(id: int = Query(..., description="ID жильца"),
                          number_of_month_paid: int = Query(gt=0, description="Количество месяцев оплаты"), payment_date: date = Query(..., description="Дата оплаты")):
    return await insert_payment(id, number_of_month_paid, payment_date)
@router.post('/insert_cost_per_month')
async def insert__cost_per_month(cost_per_month: CostPerMonthPostDTO):
    await insert_cost_per_month(cost_per_month)
@router.get('/furniture')
async def get_furniture():
    return await select_furniture()
@router.post('/insert_furniture')
async def insert_furniture_(new_furniture: FurniturePostDTO):
    await insert_furniture(new_furniture)
@router.delete('/furniture/{id}')
async def delete_furniture_(id: int):
    await delete_furniture(id)
