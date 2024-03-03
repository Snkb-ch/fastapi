import sqlalchemy.orm
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from config import ConfigDict


SQLALCHEMY_DATABASE_URL = f'postgresql://{ConfigDict["database_username"]}:{ConfigDict["database_password"]}@{ConfigDict["database_host"]}:{ConfigDict["database_port"]}/{ConfigDict["database_name"]}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
