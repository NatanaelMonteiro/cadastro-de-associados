from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from decouple import config
from app.db.models import MembersModel


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

crypt_context = CryptContext(schemes=["sha256_crypt"])


user_already_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Este email já está cadastrado."
)

user_update_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Falha na atualização do cadastro."
)


invalid_fields_len = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Todos os campos do formulário devem ser preenchidos."
)


class MemberServices:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def as_dict(self, rows):
        dados = [row._asdict() for row in rows]
        return dados
    
    #from DB
    def get_me(self):
        email = ""
        member_on_db = (
            self.db_session.query(MembersModel).filter_by(email=email).first()
        )
        return member_on_db

    #from DB
    def get_member(self, email):
        member_on_db = (
            self.db_session.query(MembersModel).filter_by(email=email).first()
        )
        return member_on_db

    # registrar membro no sistema
    def member_register(self, user, form_data):
        if (len(form_data) < 14):
            raise invalid_fields_len
        
        member_model = MembersModel()
        member_model.from_dict(form_data)
        member_model.email = user

        try:
            self.db_session.add(member_model)
            self.db_session.commit()
        except IntegrityError:
            raise user_already_exists

    # atualizar membro no sistema
    def member_update(self, user, form_data):
        if (len(form_data) < 14):
            raise invalid_fields_len
        
        try:
            query = update(MembersModel).where(
                MembersModel.email == user).values(form_data)
            self.db_session.execute(query)
            self.db_session.commit()
        except IntegrityError as e:
            raise user_update_error
