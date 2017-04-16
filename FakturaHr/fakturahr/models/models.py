# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Boolean, MetaData, UnicodeText, Unicode, ForeignKey, Float, Numeric
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from colander import null
from fakturahr.utility.helper import now, get_number_formatted
from fakturahr.models.database import Base


class Client(Base):
    name = Column(Unicode(1024), nullable=False)
    address = Column(Unicode(1024), nullable=True)
    city = Column(Unicode(1024), nullable=True)
    postal_code = Column(Unicode(1024), nullable=True)
    oib = Column(Unicode(20), nullable=True)

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
    salt = Column(Unicode(256), nullable=False)
    company_name = Column(Unicode(1024), nullable=False)
    address = Column(Unicode(1024), nullable=False)
    city = Column(Unicode(1024), nullable=False)
    post_number = Column(Unicode(512), nullable=False)
    telephone = Column(Unicode(1024), nullable=False)
    mobile_phone = Column(Unicode(1024), nullable=False)
    oib = Column(Unicode(11), nullable=False)
    iban = Column(Unicode(34), nullable=False)

    def get_fullname(self):
        return u'{0} {1}'.format(self.firstname, self.lastname)


class Item(Base):
    name = Column(Unicode(2048), nullable=False)
    ean = Column(Unicode(1024), nullable=True)
    measurement_unit = Column(Unicode(128), nullable=True)
    pack_size = Column(Integer, nullable=True)
    pallete_size = Column(Integer, nullable=True)
    price = Column(Numeric(8, 2), nullable=True)

    NAME = u'Naziv'
    EAN = u'EAN'
    MEASUREMENT_UNIT = u'Mjerna jedinica'
    PACK_SIZE = u'Pakiranje u kartonu'
    PALLETE_SIZE = u'Komada na paleti'
    PRICE = u'Cijena'
    PRICE_SUM = u'Iznos'

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
            return float(self.price)
        else:
            return None

    def get_price_formatted(self):
        if self.price is not None:
            return get_number_formatted(self.price)
        else:
            u'Nema cijenu'

    def get_value_or_null(self, value):
        if value is not None:
            return value
        return null

    def get_appstruct(self):
        return {
            'name': self.name,
            'ean': self.get_value_or_null(self.ean),
            'measurement_unit': self.get_value_or_null(self.measurement_unit),
            'pack_size': self.get_value_or_null(self.pack_size),
            'pallete_size': self.get_value_or_null(self.pallete_size),
            'price': self.get_value_or_null(self.price),
        }


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
    client_id = Column(ForeignKey('client.id'), index=True)

    user = relationship('User')
    client = relationship('Client')

    CLIENT = u'Klijent'

    TAX_PERCENT = 25
    RETURN_AMOUNT = 0.5

    date_format = u'%d.%m.%Y.'

    @classmethod
    def get_payment_option_dict(cls):
        return {
            cls.SLIP: u'Transakcijski račun (virman)'
        }

    def get_number(self):
        if self.number is not None:
            return self.number
        return u'Nema broj'

    def get_issued_date(self):
        if self.issued_date:
            return self.issued_date.strftime(self.date_format)
        else:
            u'Nema datum izdavanja'

    def get_currency_date(self):
        if self.currency_date:
            return self.currency_date.strftime(self.date_format)
        else:
            u'Nema datum valute'

    def get_issued_time(self):
        if self.issued_time:
            return self.issued_time
        else:
            return u'Nema vrijeme izdavanja'

    def get_issued_location(self):
        if self.issued_location:
            return self.issued_location
        else:
            return u'Nema mjesto izdavanja'

    def get_payment_type(self):
        if self.payment_type is not None:
            return self.get_payment_option_dict().get(self.payment_type)
        return u'Nema način plaćanja'

    def get_tax_percent(self):
        if self.tax_percent is not None:
            return self.tax_percent
        else:
            u'Nema PDV (%)'

    def get_tax_percent_formatted(self):
        if self.tax_percent is not None:
            return get_number_formatted(self.tax_percent)
        else:
            u'Nema PDV (%)'

    def get_base_amount(self):
        if self.base_amount is not None:
            return str(self.base_amount)
        else:
            u'Nema osnovicu'

    def get_base_amount_formatted(self):
        if self.base_amount is not None:
            return get_number_formatted(str(self.base_amount))
        else:
            u'Nema osnovicu'

    def get_tax_amount(self):
        if self.tax_amount is not None:
            return str(self.tax_amount)
        else:
            u'Nema iznos poreza'

    def get_tax_amount_formatted(self):
        if self.tax_amount is not None:
            return get_number_formatted(str(self.tax_amount))
        else:
            u'Nema iznos poreza'

    def get_return_amount(self):
        if self.return_amount is not None:
            return str(self.return_amount)
        else:
            u'Nema povratnu naknadu'

    def get_return_amount_formatted(self):
        if self.return_amount is not None:
            return get_number_formatted(str(self.return_amount))
        else:
            u'Nema povratnu naknadu'

    def get_total_amount(self):
        if self.total_amount is not None:
            return str(self.total_amount)
        else:
            return u'Nema ukupan iznos'

    def get_total_amount_formatted(self):
        if self.total_amount is not None:
            return get_number_formatted(str(self.total_amount))
        else:
            return u'Nema ukupan iznos'

    def get_buyer_name(self):
        if self.buyer_name:
            return self.buyer_name
        return u'Nema ime kupca'

    def get_operator(self):
        if self.user_id:
            return self.user.get_fullname()
        else:
            u'Nema operatera'

    def get_client(self):
        if self.client_id:
            return self.client.get_name()
        else:
            u'Nema klijenta'

    def get_receipt_items_indexed(self):
        receipt_items = self.items.filter(ReceiptItem.deleted == False).order_by(ReceiptItem.id.asc())
        return {index: receipt_item
                for index, receipt_item in enumerate(receipt_items)
                }

    def get_receipt_item_quantity_total(self):
        quantity_total = 0
        receipt_items = self.items.filter(ReceiptItem.deleted == False).all()
        for receipt_item in receipt_items:
            if receipt_item.quantity:
                quantity_total += receipt_item.quantity
        return quantity_total


class ReceiptItem(Base):
    name = Column(Unicode(2048), nullable=False)
    ean = Column(Unicode(1024), nullable=True)
    measurement_unit = Column(Unicode(128), nullable=True)
    pack_size = Column(Integer, nullable=True)
    pallete_size = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)
    rebate_percent = Column(Float, nullable=False, default=0.0)
    item_price = Column(Numeric(8, 2), nullable=False)
    item_price_sum = Column(Numeric(8, 2), nullable=False)

    receipt_id = Column(ForeignKey('receipt.id'), index=True)
    item_id = Column(ForeignKey('item.id'), index=True)

    receipt = relationship('Receipt', backref=backref('items', lazy='dynamic'))
    item = relationship('Item')

    QUANTITY = u'Količina'
    REBATE_PERCENT = u'Rabat'
