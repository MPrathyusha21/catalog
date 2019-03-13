import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class GmailUser(Base):
    __tablename__ = 'gmailuser'
    id = Column(Integer, primary_key=True)
    name = Column(String(260), nullable=False)
    email = Column(String(220), nullable=False)


class BookYard(Base):
    __tablename__ = 'bookyard'
    id = Column(Integer, primary_key=True)
    name = Column(String(270), nullable=False)
    user_id = Column(Integer, ForeignKey('gmailuser.id'))
    user = relationship(GmailUser, backref="bookyard")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class BookName(Base):
    __tablename__ = 'bookname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    year = Column(String(150))
    booktype = Column(String(550))
    author = Column(String(150))
    price = Column(String(10))
    bookyardid = Column(Integer, ForeignKey('bookyard.id'))
    bookyard = relationship(
        BookYard, backref=backref('bookname', cascade='all, delete'))
    gmailuser_id = Column(Integer, ForeignKey('gmailuser.id'))
    gmailuser = relationship(GmailUser, backref="bookname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
           'name': self. name,
           'year': self. year,
           'booktype': self. booktype,
           'author': self.author,
           'price': self. price,
           'id': self. id
        }

engin = create_engine('sqlite:///bookyard.db')
Base.metadata.create_all(engin)
