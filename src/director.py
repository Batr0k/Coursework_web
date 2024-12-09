from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi import Request
from src.orm.director_orm import select_workers, select_position_at_work, insert_worker
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