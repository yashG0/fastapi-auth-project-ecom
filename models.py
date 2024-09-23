from sqlalchemy import Column, ForeignKey,Integer,String
from .db import Base
from sqlalchemy.orm import relationship


class Products(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(500))
    price = Column(Integer, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String(50), nullable=False)
    userId = Column(Integer, ForeignKey('users.id'))

    owner = relationship('Users', back_populates='products')

    

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(22), nullable=False, unique=True, index=True)
    email = Column(String(35), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    products = relationship('Products', back_populates='owner')
