from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.depends import get_db_session, get_body, token_verifier
from app.services.user_services import UserServices
from app.services.member_services import MemberServices
from app.schemas import User

user = APIRouter(prefix="/user")


@user.post("/register")
def user_register(
    form_data=Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    service = UserServices(db_session=db_session)
    service.user_register(form_data)

    html = "<script>location.href='/static/cadastrar.html'</script>"
    response = HTMLResponse(html, status_code=status.HTTP_200_OK)

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
        secure=True,
        max_age=(2 * 3600),
        expires=(2 * 3600),
        samesite="lax",
        path="/",  # para o site todo
    )
    return response


@user.post("/login")
def user_register(
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
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user email"
        )

    jwt_token = service.user_login(user=user)

    html = "<script>location.href='/static/index.html'</script>"
    response = HTMLResponse(html, status_code=status.HTTP_200_OK)

    response.set_cookie(
        key="access_token",
        value="Bearer {}".format(jsonable_encoder(jwt_token)),
        httponly=True,
        secure=True,
        max_age=(2 * 3600),
        expires=(2 * 3600),
        samesite="lax",
        path="/",  # para o site todo
    )
    return response


@user.get("/logout")
async def logout(request: Request):
    response = HTMLResponse("<script>location.href='/static/index.html'</script>")
    response.delete_cookie("access_token")
    return response


@user.get("/is_login", response_class=HTMLResponse)
async def is_login(request: Request, db_session=Depends(get_db_session)):
    try:
        token = token_verifier(request)
        service = UserServices(db_session=db_session)
        user = token.get("sub")
        service = MemberServices(db_session)
        member = service.get_member(user)

        # if member is None:
        #     return HTMLResponse("<script>location.href='/static/index.html'</script>")
        # else:
        return """
            <a href="/user/logout"
                class="px-3 text-white bg-primary nav-link rounded-3 text-base leading-6 fw-semibold text-center">
                Sair
            </a>
            """
    except:
        return """
            <a href="/static/login.html"
                class="px-3 text-white bg-primary nav-link rounded-3 text-base leading-6 fw-semibold text-center">
                Entrar
            </a>
            """
