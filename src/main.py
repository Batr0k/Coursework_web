from fastapi import FastAPI, Request, Response, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from src.komendant import router as komendant_router
from src.accountant import router as accountant_router
from src.director import router as director_router
from src.schemas.auth_schemas import UserDTO
from datetime import timedelta, datetime, UTC
from src.orm.auth_orm import verify_password, find_user
DOMEN = "http://127.0.0.1:8000/"
def get_token_from_cookie(request: Request):
    token = request.cookies.get("auth_token")
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No auth token in cookies")
    return token


async def is_komendant(request: Request):
    token = get_token_from_cookie(request)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token == "komendant":
        return token
    raise credentials_exception

async def is_accountant(request: Request):
    token = get_token_from_cookie(request)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token == "accountant":
        return token
    raise credentials_exception
async def is_director(request: Request):
    token = get_token_from_cookie(request)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if token == "director":
        return token
    raise credentials_exception
app = FastAPI()
app.include_router(komendant_router, dependencies=[Depends(is_komendant)])
app.include_router(accountant_router, dependencies=[Depends(is_accountant)])
app.include_router(director_router, dependencies=[Depends(is_director)])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})
@app.post('/login')
async def login(response: Response, user_dto: UserDTO):
    user = await find_user(user_dto.login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(user_dto.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    expires = datetime.now(UTC) + timedelta(minutes=1)
    response.set_cookie(
        key="auth_token",
        value=user.login,
        httponly=True,
        expires=expires
    )
    return { "login": user.login }

@app.get('/logout')
async def logout(response: Response):
    response.delete_cookie(key="auth_token")
    return {"message": "Cookie deleted"}