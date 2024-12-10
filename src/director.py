from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request, Query
from src.orm.director_orm import (select_workers, select_position_at_work, insert_worker, delete_worker, get_worker,
                                  update_worker, update_position_at_work)
from src.schemas.director_schemas import WorkerPostDTO

router = APIRouter(prefix="/director")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("director-page.html",
                                      {"request": request})
@router.get('/workers')
async def get_workers():
    return await select_workers()
@router.get('/position_at_work')
async def get_position_at_work():
    return await select_position_at_work()
@router.post('/workers')
async def insert_worker_(worker: WorkerPostDTO):
    await insert_worker(worker)
@router.delete('/workers/{id}')
async def delete_workers_(id:int):
    await delete_worker(id)

@router.get('/workers/{id}')
async def get_worker_(id: int):
    return await get_worker(id)
@router.put('/workers/{id}')
async def update_worker_(id: int, worker: WorkerPostDTO):
    return await update_worker(id, worker)
@router.put('/position_at_work/{id}')
async def update_position_at_work_(id: int, salary: int = Query(gt=0)):
    await update_position_at_work(id, salary)

