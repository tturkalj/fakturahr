from sqlalchemy import create_engine, MetaData, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from fakturahr.utility.helper import now


class BaseModel(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, nullable=False, default=now())
    last_changed_date = Column(DateTime, nullable=False, default=now())
    deleted = Column(Boolean, nullable=False, default=False)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s"
}
engine = create_engine('sqlite+pysqlite:///fakturahr.db', convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=True, autoflush=False, bind=engine))
Base = declarative_base(cls=BaseModel)
Base.metadata = MetaData(naming_convention=naming_convention)
Base.query = Session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from fakturahr.models import models
    Base.metadata.create_all(bind=engine, checkfirst=True)