from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean
import os

import settings

DeclarativeBase = declarative_base()


def db_connect(db):
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    if db is "local":
        return create_engine(URL(**settings.DATABASE))
    elif db is "heroku":
        return create_engine(URL(os.environ['DATABASE_URL']))


def create_adverts_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class CarAdverts(DeclarativeBase):
    """Sqlalchemy caradverts model"""
    __tablename__ = "car_adverts_table"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    price = Column('price', String, nullable=True)
    year = Column('year', String, nullable=True)
    location = Column('location', String, nullable=True)
    link = Column('link', String, nullable=True)
    date = Column('date', String, nullable=True)
    mailsent = Column('mailsent', Boolean, nullable=False, default=False)
    isvalid = Column('isvalid', Boolean, nullable=True, default=True)

    def getInfo(self):
        return self.title, self.price, self.year, self.location, self.link, self.date