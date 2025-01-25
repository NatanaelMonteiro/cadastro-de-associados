# import os
from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = config("DB_URL")
# DB_URL = config(os.environ.get("DB_URL"))

engine = create_engine(DB_URL, pool_pre_ping=True)
DBSession = sessionmaker(bind=engine)
