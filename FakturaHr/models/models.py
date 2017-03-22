from sqlalchemy import Column, DateTime, Integer, Boolean, MetaData, UnicodeText, Unicode, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from search_engine_app.helper import now


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, nullable=False, default=now())
    last_changed_date = Column(DateTime, nullable=False, default=now())
    deleted = Column(Boolean, nullable=False, default=False)


class Client(BaseModel):
    name = Column(Unicode(1024), nullable=False)
    address = Column(Unicode(1024), nullable=False)
    city = Column(Unicode(1024), nullable=False)
    postal_code = Column(Unicode(1024), nullable=False)
    oib = Column(Unicode(20), nullable=False)
    company_id = Column(ForeignKey('company.id'), index=True)


class User(BaseModel):
    firstname = Column(Unicode(1024), nullable=False)
    lastname = Column(Unicode(1024), nullable=False)
    email = Column(Unicode(1024), nullable=False)
    password = Column(Unicode(512), nullable=False)
    hash = Column(Unicode(128), nullable=False)
    company_id = Column(ForeignKey('company.id'), index=True)


class Company(BaseModel):
    name = Column(Unicode(1024), nullable=False)


class Item(BaseModel):
    name = Column(UnicodeText, nullable=False)
    ean = Column(Unicode(1024), nullable=False)
    measurement_unit = Column(Unicode(128), nullable=False)
    pack_size = Column(Integer, nullable=False)
    pallete_size = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)