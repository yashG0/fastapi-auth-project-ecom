from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLITE_DB_LINK = "sqlite:///./ecom.db"

engine = create_engine(SQLITE_DB_LINK, connect_args={"check_same_thread":False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getDb():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
