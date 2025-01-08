from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
from sqlalchemy.orm import Session
from app.depends import token_verifier, get_db_session, get_body
from app.services.user_services import UserServices
from app.services.member_services import MemberServices

api = APIRouter(prefix="/api", dependencies=[Depends(token_verifier)])

CADAS_URL = """<a class="link" href="/static/cadastrar.html">Cadastro</a>"""
EDIT_URL = """<a class="link" href="/static/editar.html">Cadastro</a>"""

@api.post("/members")
def member_register(
    request: Request,
    form_member=Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    access_token = request.cookies.get("access_token")
    user_service = UserServices(db_session=db_session)
    user = user_service.get_user_on_token(access_token)

    member_service = MemberServices(db_session=db_session)
    member_service.member_register(user, form_member)
    return JSONResponse(content="Cadastro incluído.", status_code=status.HTTP_201_CREATED)

@api.put("/members")
def member_register(
    request: Request,
    form_member=Depends(get_body),
    db_session: Session = Depends(get_db_session),
):
    access_token = request.cookies.get("access_token")
    user_service = UserServices(db_session=db_session)
    user = user_service.get_user_on_token(access_token)

    member_service = MemberServices(db_session=db_session)
    member_service.member_update(user, form_member)
    return JSONResponse(content="Cadastro atualizado.", status_code=status.HTTP_202_ACCEPTED)


@api.get("/members/exists")
def member_by_email(request: Request, db_session: Session = Depends(get_db_session)):
    service = MemberServices(db_session)
    username = get_user_name(request, db_session)
    member = service.get_member(username)

    if member is None:
        return HTMLResponse(CADAS_URL)
    else:
        return HTMLResponse(EDIT_URL)


@api.get("/members/{email}", response_class=PlainTextResponse)
def get_member(email, db_session: Session = Depends(get_db_session)):
    service = MemberServices(db_session=db_session)
    return service.get_member(email)


@api.get("/user_name", response_class=PlainTextResponse)
def get_user_name(request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session=db_session)
    username = service.get_user_on_token(access_token)
    return username

@api.get("/me", response_class=JSONResponse)
def get_me(request: Request, db_session: Session = Depends(get_db_session)):
    email = get_user_name(request)
    service = MemberServices(db_session=db_session)
    member = service.get_member(email)
    return member
