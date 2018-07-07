#!/usr/bin/env python

from sqlalchemy import Column, Integer, Numeric, String, Sequence, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.event import listen
from sqlalchemy import event, DDL
from db import session

Base = declarative_base()

class ProductsTbl(Base):
    __tablename__ = 'products'

    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    name = Column(String(255))
    price = Column(Numeric)
    stock = Column(Integer)

    status_id = Column(Integer, ForeignKey("product_status.id"))
    status = relationship("ProductStatus", foreign_keys=[status_id])

class ProductStatus (Base):
    __tablename__ = 'product_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class TransactionsTbl (Base):
    __tablename__ = 'transactions'


    id = Column(Integer, Sequence('transaction_id_seq'), primary_key=True)
    name = Column(String)
    date_created = Column(DateTime)
    date_arrived = Column(DateTime)
    date_shipped = Column(DateTime)
    total = Column(Numeric)

    status_id = Column(Integer, ForeignKey("transaction_status.id"))
    status = relationship("TransactionStatus", foreign_keys=[status_id])

class TransactionStatus (Base):
    __tablename__ = 'transaction_status'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))

class TransactionProducts (Base):
    __tablename__ = 'transaction_products';

    id = Column(Integer, Sequence('transaction_product_id_seq'), primary_key=True)
    amount = Column(Integer)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    product_id = Column(Integer, ForeignKey("products.id"))


    transaction = relationship("TransactionsTbl", foreign_keys=[transaction_id])
    product = relationship("ProductsTbl", foreign_keys=[product_id])

def insert_product_status_values(*args, **kwargs):
    session.add(ProductStatus(name='ACTIVE'))
    session.add(ProductStatus(name='INACTIVE'))
    session.commit()

def insert_transaction_status_values(*args, **kwargs):
    session.add(TransactionStatus(name='CREATED'))
    session.add(TransactionStatus(name='ONGOING'))
    session.add(TransactionStatus(name='COMPLETED'))
    session.add(TransactionStatus(name='CANCELLED'))
    session.commit()

event.listen(ProductStatus.__table__, 'after_create', insert_product_status_values)
event.listen(TransactionStatus.__table__, 'after_create', insert_transaction_status_values)


from sqlalchemy import create_engine
from settings import DB_URI
engine = create_engine(DB_URI)

# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
