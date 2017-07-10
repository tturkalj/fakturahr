# -*- coding: utf-8 -*-
import transaction
from fakturahr.models.database import Session
from fakturahr.models.models import User


def init_db():
    with transaction.manager:
        user = Session.query(User).filter(User.firstname == u'Tomi').first()
        if not user:
            user = User()
            user.firstname = u'Tomi'
            user.lastname = u'Turki'
            user.email = u'mail@mail.com'
            user.company_name = u'TURKi, OBRT ZA TRGOVINU'
            user.city = u'ZAGREB'
            user.address = u'ZAGREB'
            user.post_number = u'10090'
            user.telephone = u''
            user.mobile_phone = u''
            user.oib = u''
            user.iban = u''
            user.password = u'pass'
            user.salt = u'salt'
            Session.add(user)
            Session.flush()

