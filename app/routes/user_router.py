from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session, get_body, token_verifier
from app.services.user_services import UserServices
from app.services.member_services import MemberServices
from app.schemas import User

user = APIRouter(prefix="/user")

INDEX_URL = """<script>location.href="/static/index.html"</script>"""
CADAS_URL = """<script>location.href="/static/cadastrar.html"</script>"""
LOGIN_URL = """<a class="link" href="/static/login.html">Entrar</a>"""
LOGOUT_URL = """<a class="link" href="/user/logout">Sair</a>"""
JOINUS_URL = """<a class="link" href="/static/login.html">Junte-se a nós!</a>"""
WELCOME_URL = """<a class="about" href="#about">Seja bem vindo!</a>"""


@user.post("/register")
def user_register(
    form_data=Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    service.user_register(form_data)
    response = HTMLResponse(CADAS_URL, status_code=status.HTTP_200_OK)

    user = User(
        username=form_data.get("username"),
        password=form_data.get("password"),
        permissions="",
    )
    jwt_token = service.user_login(user=user)

    response.set_cookie(
        key="access_token",
        value="Bearer {}".format(jsonable_encoder(jwt_token)),
        httponly=True,
        secure=False,
        max_age=(2 * 3600),
        expires=(2 * 3600),
        samesite="lax",
    )
    return response


@user.post("/login")
def login(
    form_user: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)

    try:
        user = User(
            username=form_user.username, password=form_user.password, permissions=""
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email inválido."
        )

    jwt_token = service.user_login(user=user)

    response = HTMLResponse(INDEX_URL, status_code=status.HTTP_200_OK)

    response.set_cookie(
        key="access_token",
        value="Bearer {}".format(jsonable_encoder(jwt_token)),
        httponly=True,
        secure=False,
        max_age=(2 * 3600),
        expires=(2 * 3600),
        samesite="lax",
    )
    return response


@user.get("/logout")
async def logout(request: Request):
    response = HTMLResponse(INDEX_URL, status_code=status.HTTP_200_OK)
    response.delete_cookie("access_token")
    return response


@user.get("/is_login", response_class=HTMLResponse)
async def is_login(request: Request, db_session=Depends(get_db_session)):
    try:
        token_verifier(request)
        return LOGOUT_URL
    except:
        return LOGIN_URL


@user.get("/is_logged")
async def is_logged(request: Request, db_session=Depends(get_db_session)):
    try:
        token_verifier(request)
        return JSONResponse({"msg": "OK"})
    except:
        return JSONResponse(None)


@user.get("/welcome", response_class=HTMLResponse)
async def welcome(request: Request, db_session=Depends(get_db_session)):
    try:
        token_verifier(request)
        return WELCOME_URL
    except:
        return JOINUS_URL
