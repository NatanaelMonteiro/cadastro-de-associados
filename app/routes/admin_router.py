from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.depends import admin_verifier, get_db_session
from app.services.user_services import UserServices


admin = APIRouter(prefix="/admin", dependencies=[Depends(admin_verifier)])

@admin.get("/admin_page")
def get_admin_page():
    restrito = '<a class="link" href="admin.html">Área restrita</a>'
    return HTMLResponse(restrito, status_code=status.HTTP_200_OK)

@admin.get("/users", response_class=JSONResponse)
def get_users_list(db_session: Session = Depends(get_db_session)):
    service = UserServices(db_session=db_session)
    users = service.get_users_list()
    return users