from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.depends import admin_verifier, get_db_session
from app.services.user_services import UserServices
from app.services.member_services import MemberServices


admin = APIRouter(prefix="/admin", dependencies=[Depends(admin_verifier)])

err_self_remove = HTTPException(
    detail="Não é permitido excluir seu próprio cadastro.",
    status_code=status.HTTP_401_UNAUTHORIZED,
)

err_self_downgrade = HTTPException(
    detail="Não é permitido excluir seus próprios poderes.",
    status_code=status.HTTP_401_UNAUTHORIZED,
)


@admin.get("/is_admin")
def is_admin():
    return JSONResponse(None, status_code=status.HTTP_200_OK)


@admin.get("/members", response_class=JSONResponse)
def get_members_list(db_session: Session = Depends(get_db_session)):
    service = MemberServices(db_session=db_session)
    return service.get_members()


@admin.get("/users", response_class=JSONResponse)
def get_users_list(db_session: Session = Depends(get_db_session)):
    service = UserServices(db_session=db_session)
    users = service.get_users_list()
    return users


@admin.patch("/users/{username}/admin", response_class=JSONResponse)
def set_user_admin(username, db_session: Session = Depends(get_db_session)):
    service = UserServices(db_session=db_session)
    user = service.get_user(username)
    user.permissions = "admin"
    service.update_user(user)

    users = service.get_users_list()
    return users


@admin.patch("/users/{username}/admin/remove", response_class=JSONResponse)
def unset_user_admin(
    username, request: Request, db_session: Session = Depends(get_db_session)
):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session=db_session)
    me = service.get_user_on_token(access_token)

    if me == username:
        raise err_self_downgrade

    user = service.get_user(username)
    user.permissions = None
    service.update_user(user)

    users = service.get_users_list()
    return users


@admin.delete("/users/{username}", response_class=HTMLResponse)
def del_user(username, request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session=db_session)
    me = service.get_user_on_token(access_token)

    if me == username:
        raise err_self_remove

    service.delete_user(username)

    return None
