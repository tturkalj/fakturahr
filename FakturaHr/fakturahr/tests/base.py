from unittest import TestCase
from sqlalchemy import create_engine, MetaData, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from fakturahr.utility.helper import now
from fakturahr.models.database import Session
from fakturahr.app import create_app
from fakturahr.utility.init_db import init_db
from fakturahr import get_root_path
from fakturahr import config

class BaseTestCase(TestCase):
    def setUp(self):
        engine = create_engine('sqlite+pysqlite:///{0}'.format(config.TEST_DB_NAME), convert_unicode=True)
        Session.configure(engine=engine)
        session_maker = sessionmaker(autocommit=True, autoflush=False, bind=engine)
        session = session_maker()
        init_db()
        app = create_app()
        app.testing = True
        self.app = app.test_client()

    def tearDown(self):








