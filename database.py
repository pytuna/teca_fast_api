from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# ket noi database
conn_text = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
    'root', 'Trungnam.1611', 'localhost', 'teca'
)
engine =  create_engine(conn_text)
# engine.connect()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class DBContext:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, et, ev, traceback):
        self.db.close()