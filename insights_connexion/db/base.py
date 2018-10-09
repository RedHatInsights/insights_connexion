from ..config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
session = None


def init():
    global session
    engine = create_engine(
        'postgresql://{}:{}@{}:{}/{}'.format(config.db_user, config.db_password,
                                             config.db_host, config.db_port, config.db_name),
        pool_size=int(config.db_pool_size),
        max_overflow=int(config.db_max_overflow))
    session = scoped_session(sessionmaker(
        autocommit=False, autoflush=False, bind=engine))
    Base.query = session.query_property()
    Base.metadata.create_all(engine)
    return session
