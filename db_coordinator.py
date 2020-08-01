from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    title = Column('title', String(32))
    in_stock = Column('in_stock', Boolean)
    quantity = Column('quantity', Integer)
    price = Column('price', Numeric)


class Type(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True)
    name = Column(String)



class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Element(Base):
    __tablename__ = 'elements'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Rarity(Base):
    __tablename__ = 'rarity'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Power(Base):
    __tablename__ = 'power'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Set(Base):
    __tablename__ = 'sets'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class full_art(Base):
    __tablename__ = 'full_art'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class thumb_art(Base):
    __tablename__ = 'thumb_art'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = relationship("Type")
    job = Column(String)
    element = Column(String)
    cost = Column(Integer)
    rarity = Column(String)
    power = Column(Integer)
    category = Column(String)
    set = Column(String)
    code = Column(String)
    full_art = Column(String)
    thumb_art = Column(String)
