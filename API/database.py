from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database


engine = create_engine("mysql+pymysql://user:password@localhost/vias_database")

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()

# Dependency
if not database_exists(engine.url):
    create_database(engine.url)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()