# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Integer, Boolean, MetaData, UnicodeText, Unicode, ForeignKey, Float, Numeric
from sqlalchemy.orm import relationship
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
            'oib': self.get_value_or_null(self.oib),
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
    name = Column(Unicode(2048), nullable=False)
    ean = Column(Unicode(1024), nullable=True)
    measurement_unit = Column(Unicode(128), nullable=True)
    pack_size = Column(Integer, nullable=True)
    pallete_size = Column(Integer, nullable=True)
    price = Column(Numeric(8, 2), nullable=True)

    def get_name(self):
        if self.name:
            return self.name
        return u'Nema ime'

    def get_ean(self):
        if self.ean is not None:
            return self.ean
        return u'Nema EAN'

    def get_measurement_unit(self):
        if self.measurement_unit is not None:
            return self.measurement_unit
        return u'Nema mjernu jedinicu'

    def get_pack_size(self):
        if self.pack_size is not None:
            return self.pack_size
        return u'Nema broj u pakiranju'

    def get_pallete_size(self):
        if self.pallete_size is not None:
            return self.pallete_size
        return u'Nema broj na paleti'

    def get_price(self):
        if self.price is not None:
            return u'{:0.2f}'.format(self.price)
        else:
            u'Nema cijenu'

    def get_price_formatted(self):
        if self.price is not None:
            formatted = u'{:0,.2f}'.format(self.price)
            formatted = formatted.replace(',', 'temp')
            formatted = formatted.replace('.', ',')
            formatted = formatted.replace('temp', '.')
            return formatted


class Receipt(Base):
    SLIP = 0
    number = Column(Unicode(100), nullable=False)
    issued_date = Column(DateTime, nullable=False)
    currency_date = Column(DateTime, nullable=False)
    issued_time = Column(Unicode(10), nullable=False)
    issued_location = Column(Unicode(100), nullable=False)
    payment_type = Column(Integer, nullable=False, default=SLIP)
    tax_percent = Column(Integer, nullable=False)
    base_amount = Column(Numeric(8, 2), nullable=False)
    tax_amount = Column(Numeric(8, 2), nullable=False)
    return_amount = Column(Numeric(8, 2), nullable=False)
    total_amount = Column(Numeric(8, 2), nullable=False)
    buyer_name = Column(Unicode(100), nullable=True)
    user_id = Column(ForeignKey('user.id'), index=True)

    user = relationship('User')


class ReceiptItem(Base):
    receipt_id = Column(ForeignKey('receipt.id'), index=True)

    name = Column(Unicode(2048), nullable=False)
    ean = Column(Unicode(1024), nullable=True)
    measurement_unit = Column(Unicode(128), nullable=True)
    pack_size = Column(Integer, nullable=True)
    pallete_size = Column(Integer, nullable=True)
    price = Column(Numeric(8, 2), nullable=True)

    quantity = Column(Integer, nullable=False)
    rebate_percent = Column(Integer, nullable=False, default=0)
    item_price = Column(Numeric(8, 2), nullable=False)
    item_price_sum = Column(Numeric(8, 2), nullable=False)








