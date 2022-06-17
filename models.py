from sqlalchemy import String, Integer, Column, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True,index = True, nullable = False)
    username = Column(String(16), unique=True,index = True, nullable = False)
    hashed_password = Column(String(128), nullable = False)
    role = Column(Boolean, nullable = False)


# alembic init alembic -- sua file duong dan mysql, import vao file env.py tu model ==> Base
# alembic revision --autogenerate -m "First revision" -- tao code auto
# alembic upgrade "ten file" -- chay file auto  --> check trong database
# alembic downgrade -1 -- tro ve file auto dau tien