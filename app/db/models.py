from sqlalchemy import Column, String, Integer, Date 
from sqlalchemy.orm import declarative_base


class CommonBase(object):
    def from_dict(self, form_data):
        if isinstance(form_data, dict):
            for key, value in form_data.items():
                setattr(self, key, value)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def to_number(self, text):
        return ''.join(c for c in str(text) if c.isdigit())


Base = declarative_base(cls=CommonBase)


class UserModel(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column("username", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    permissions = Column("permissions", String, nullable=True)


class MembersModel(Base):
    __tablename__ = "members"
    id = Column("id", Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    nome_guerra = Column("nome_guerra", String, nullable=False)
    patente = Column("patente", String, nullable=False)
    cpf = Column("cpf", String, nullable=False, unique=True)
    rg = Column("rg", String, nullable=False)
    dt_nasc = Column("dt_nasc", String, nullable=False)
    lotacao = Column("lotacao", String, nullable=False)
    matricula = Column("matricula", String, nullable=False, unique=True)
    cfp_cfsd = Column("cfp_cfsd", String, nullable=False)
    telefone = Column("telefone", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    genero = Column("genero", String, nullable=False)
    pm_bm = Column("pm_bm", String, nullable=False)
    dependentes = Column("dependentes", Integer, nullable=False)
    situacao = Column("situacao", String, nullable=False)
