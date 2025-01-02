from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from app.depends import admin_verifier, get_db_session
from app.services.user_services import UserServices


admin = APIRouter(prefix="/admin", dependencies=[Depends(admin_verifier)])

@admin.get("/testar", response_class=PlainTextResponse)
def testar_admin():
    return "Este endpoint só é acessível por alguém com perfil ADMIN."

@admin.get("/users")
def get_users_list(db_session: Session = Depends(get_db_session)):
    service = UserServices(db_session=db_session)
    users = service.get_users_list()
    return JSONResponse({"message":"Usuario ADMIN", "dados": users})