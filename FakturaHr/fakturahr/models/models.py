# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Integer, Boolean, MetaData, UnicodeText, Unicode, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from colander import null
from fakturahr.utility.helper import now
from fakturahr.models.database import Base


class Client(Base):
    name = Column(Unicode(1024), nullable=False)
    address = Column(Unicode(1024), nullable=True)
    city = Column(Unicode(1024), nullable=True)
    postal_code = Column(Unicode(1024), nullable=True)
    oib = Column(Unicode(20), nullable=True)
    company_id = Column(ForeignKey('company.id'), index=True)

    def __init__(self, appstruct=None):
        if appstruct:
            for key in appstruct:
                if hasattr(self, key):
                    if appstruct[key] == null:
                        setattr(self, key, None)
                    else:
                        setattr(self, key, appstruct[key])

    def get_name(self):
        if self.name:
            return self.name
        return u'Nema ime'

    def get_address(self):
        if self.address is not None:
            return self.address
        else:
            return u'Nema adrese'

    def get_city(self):
        if self.city is not None:
            return self.city
        else:
            return u'Nema grada'

    def get_postal_code(self):
        if self.postal_code is not None:
            return self.postal_code
        else:
            return u'Nema poštanskog broja'

    def get_oib(self):
        if self.oib is not None:
            return self.oib
        else:
            return u'Nema OIB'

    def get_value_or_null(self, value):
        if value is not None:
            return value
        return null

    def get_appstruct(self):
        return {
            'name': self.name,
            'address': self.get_value_or_null(self.address),
            'city': self.get_value_or_null(self.city),
            'postal_code': self.get_value_or_null(self.postal_code),
            'company_id': self.get_value_or_null(self.company_id),
        }

    def edit_appstruct(self, appstruct):
        edited = False
        for key in appstruct:
            if hasattr(self, key):
                if appstruct[key] != null:
                    if getattr(self, key) != appstruct[key]:
                        setattr(self, key, appstruct[key])
                        edited = True
                else:
                    if getattr(self, key) is not None:
                        setattr(self, key, appstruct[key])
                        edited = True
        return edited





class User(Base):
    firstname = Column(Unicode(1024), nullable=False)
    lastname = Column(Unicode(1024), nullable=False)
    email = Column(Unicode(1024), nullable=False)
    password = Column(Unicode(512), nullable=False)
    hash = Column(Unicode(128), nullable=False)
    company_id = Column(ForeignKey('company.id'), index=True)


class Company(Base):
    name = Column(Unicode(1024), nullable=False)


class Item(Base):
    name = Column(UnicodeText, nullable=False)
    ean = Column(Unicode(1024), nullable=True)
    measurement_unit = Column(Unicode(128), nullable=True)
    pack_size = Column(Integer, nullable=True)
    pallete_size = Column(Integer, nullable=True)
    price = Column(Float, nullable=True)
