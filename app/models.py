from .database import Base
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship

class User(Base) :
    __tablename__ = "users2"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(300), nullable=False)
    role = Column(Integer, nullable=False)
