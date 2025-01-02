from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.connection import DBSession
from app.services.user_services import UserServices
import urllib.parse as parse
import json


def get_db_session():
    try:
        session = DBSession()
        yield session
    finally:
        session.close()


async def get_body(request: Request):
    payload = await request.body()
    payload = payload.decode("utf8")
    payload = parse.unquote(payload)

    try:
        body = json.loads(payload)
    except:
        try:
            lista = list(payload.split("&"))
            body = dict(l.split("=") for l in lista)
        except:
            body = {}

    return body


def token_verifier(request: Request, db_session: Session = Depends(get_db_session)):
    access_token = request.cookies.get("access_token")
    service = UserServices(db_session)
    return service.verify_token(access_token)


def admin_verifier(request: Request, db_session: Session = Depends(get_db_session)):
    token = token_verifier(request)
    service = UserServices(db_session)
    service.verify_user_admin(token)
