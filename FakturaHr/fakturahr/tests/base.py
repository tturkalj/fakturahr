import os
from unittest import TestCase
from sqlalchemy import create_engine, MetaData, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from fakturahr.utility.helper import now
from fakturahr.models import models
from fakturahr.models.database import Session, Base
from fakturahr.models.models import Client
from fakturahr.app import create_app
from fakturahr.utility.init_db import init_db
from fakturahr import get_root_path
from fakturahr import config


class BaseTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(config.TEST_DB_NAME) and os.path.isfile(config.TEST_DB_NAME):
            os.unlink(config.TEST_DB_NAME)

        cls.engine = create_engine('sqlite+pysqlite:///{0}'.format(config.TEST_DB_NAME), convert_unicode=True)

        Base.metadata.create_all(bind=cls.engine, checkfirst=True)

        app = create_app()
        app.testing = True
        cls.app = app.test_client()

    def setUp(self):
        self.connection = self.engine.connect()
        self.transaction = self.connection.begin()
        Session.configure(bind=self.connection)
        session_maker = sessionmaker(bind=self.connection)
        self.session = session_maker()
        init_db()

    def tearDown(self):
        Session.close()
        self.transaction.rollback()
        self.connection.close()
        self.session.close()
        Session.expire_all()
        Session.expunge_all()
        Session.close_all()
        Session.remove()

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()


    def add_client(self, name='test_client', address='test_address', city='test_city', postal_code='10000', oib='123456'):
        client = Client()
        client.name = name
        client.address = address
        client.city = city
        client.postal_code = postal_code
        client.oib = oib
        self.session.add(client)
        self.session.commit()
        return client







