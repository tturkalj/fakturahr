# -*- coding: utf-8 -*-
import transaction
from fakturahr.models.database import Session
from fakturahr.models.models import User


def init_db():
    with transaction.manager:
        user = Session.query(User).filter(User.firstname == u'Miroslav').first()
        if not user:
            user = User()
            user.firstname = u'Miroslav'
            user.lastname = u'Šebrek'
            user.email = u'miroslav.sebrek12@gmail.com'
            user.company_name = u'ŠEBREK, OBRT ZA TRGOVINU'
            user.city = u'ZAGREB - SUSEDGRAD'
            user.address = u'ŠETALIŠTE 150. BRIGADE HV 10'
            user.post_number = u'10090'
            user.telephone = u'385 1 560 2636'
            user.mobile_phone = u'385 99 3873 513'
            user.oib = u'03288364795'
            user.iban = u'HR7323600001102464487'
            user.password = u'pass'
            user.salt = u'salt'
            Session.add(user)
            Session.flush()

