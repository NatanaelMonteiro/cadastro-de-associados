from datetime import datetime, timedelta, timezone
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError

from decouple import config
from app.db.models import UserModel
from app.schemas import User


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")

crypt_context = CryptContext(schemes=["sha256_crypt"])

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Usuário não autenticado.",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_usr_or_pass = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Email ou senha inválidos.",
)

insufficient_permissions = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="O usuário sem permissão.",
)

user_already_exists = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado."
)

invalid_user_name = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Email inválido."
)


class UserServices:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def as_dict(self, rows):
        dados = [row._asdict() for row in rows]
        return dados

    def get_user(self, username):
        user_on_db = (
            self.db_session.query(UserModel).filter_by(username=username).first()
        )
        return user_on_db

    def get_users_list(self):
        users = self.db_session.query(
            UserModel.id, UserModel.username, UserModel.permissions
        ).all()
        
        return self.as_dict(users)

    # registrar usuário do sistema
    def user_register(self, form_data):
        user = None

        try:
            user = User(
                username=form_data.get("username"),
                password=form_data.get("password"),
                permissions="",
            )
        except:
            raise invalid_user_name

        user_model = UserModel(
            username=user.username, password=crypt_context.hash(user.password)
        )
        try:
            self.db_session.add(user_model)
            self.db_session.commit()
        except IntegrityError:
            raise user_already_exists

    # logar e devolver o token
    def user_login(self, user: User, expires_in: int = 30):
        db_user = self.get_user(user.username)

        if db_user is None:
            raise invalid_usr_or_pass

        if not crypt_context.verify(user.password, db_user.password):
            raise invalid_usr_or_pass

        permissions = []

        if db_user.permissions:
            for p in db_user.permissions.split(" "):
                permissions.append(p)

        exp = datetime.now(timezone.utc) + timedelta(minutes=expires_in)
        payload = {"sub": user.username, "permissions": permissions, "exp": exp}
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return access_token

    # obter usuário contido no token
    def get_user_on_token(self, access_token):
        token = self.verify_token(access_token)
        return token.get("sub")

    # verificar se o Usuário contido no token tem perfil ADMIN
    def verify_user_admin(self, token):
        user = token.get("sub")
        permissions = token.get("permissions")

        if user is None or permissions is None:
            raise insufficient_permissions

        if "admin" not in permissions:
            raise insufficient_permissions

    # verificar se o token é válido, se o usuário está autenticado
    def verify_token(self, access_token):
        if access_token and access_token.startswith("Bearer "):
            access_token = access_token.split(" ")[1]

            try:
                token = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            except JWTError:
                raise invalid_token

            user = token.get("sub")

            if user is None:
                raise invalid_token

            return token

        else:
            raise invalid_token
