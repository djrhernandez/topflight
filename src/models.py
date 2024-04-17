# models.py

import os
import logging
from typing import List
from typing import Optional
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .utils import create_db_path


# Configure Python logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

connection_str = create_db_path('skyhawk.db')

engine = create_engine(connection_str, echo=False)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

def inspect_tables():
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        print(f"Table: {table_name}")
        for column in inspector.get_columns(table_name):
            print(f"Column: {column['name']} Type: {column['type']}")


def inspect_hotels():
    try:
        db_session.rollback()
        # Querying all hotel entries
        hotels = db_session.query(Hotels).all()
        for hotel in hotels:
            print(f"Hotel ID: {hotel.parid}, Owner: {hotel.owner_name}, Borough: {hotel.borough}, Address: {hotel.street_num} {hotel.street_name}, Postcode: {hotel.postcode}")
    except Exception as e:
        print(f"Error accessing database: {e}")


class Hotels(Base):
    __tablename__ = "hotel"
    
    parid = Column(Integer, primary_key=True)
    owner_name = Column(String, nullable=True)
    
    borough = Column(String, nullable=True)
    borocode = Column(Integer, nullable=True)

    street_num = Column(String, nullable=True)
    street_name = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    
    bldg_class = Column(String, nullable=True)
    bin = Column(String, nullable=True)
    block = Column(String, nullable=True)
    lot = Column(String, nullable=True)
    bbl = Column(String, nullable=True)
    taxyear = Column(String, nullable=True)
    taxclass = Column(String, nullable=True)
    community_board = Column(String, nullable=True)
    census_tract = Column(String, nullable=True)
    council_district = Column(String, nullable=True)
    nta = Column(String, nullable=True)
    nta_code2 = Column(String, nullable=True)
    
    
    # owners = relationship("Owners")
    # building_info = relationship('Building')
    # tax_info = relationship('TaxInfo', backref=backref('hotel'))
    # census_info = relationship('CensusInfo', backref=backref('hotel'))

    def __repr__(self):
        return f"<Hotel {self.id}>"


# class Owners(Base):
#     __tablename__ = "owners"
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=True)
#     # hotels = relationship("Hotel")

#     def __repr__(self):
#         return f"<Owner {self.name} ({self.id})>"


# class Borough(Base):
#     __tablename__ = 'borough'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=True)
#     borocode = Column(Integer, nullable=True)
#     # hotels = relationship('HotelModel', backref=backref('borough_id'))


# class Location(Base):
#     __tablename__ = 'location'
#     id = Column(Integer, primary_key=True)
#     number = Column(String, nullable=True)
#     name = Column(String, nullable=True)
#     zipcode = Column(String, nullable=True)
#     latitude = Column(Integer)
#     longitude = Column(Integer)


# class Building(Base):
#     __tablename__ = 'building'
#     id = Column(Integer, primary_key=True)
#     bbl = Column(Integer, nullable=True)
#     bin_number = Column(Integer, nullable=True)
#     bdlg_class = Column(String, nullable=True)
#     block = Column(Integer, nullable=True)
#     lot = Column(Integer, nullable=True)


# class TaxInfo(Base):
#     __tablename__ = 'tax_info'
#     id = Column(Integer, primary_key=True)
#     # hotel_parid = Column(Integer, ForeignKey('hotels.parid'))
#     tax_year = Column(Integer, nullable=True)
#     tax_class = Column(Integer, nullable=True)


# class CensusInfo(Base):
#     __tablename__ = 'census_info'
#     id = Column(Integer, primary_key=True)
#     # hotel_parid = Column(Integer, ForeignKey('hotels.parid'))
#     community_board = Column(Integer, nullable=True)
#     council_district = Column(Integer, nullable=True)
#     census_tract = Column(Integer, nullable=True)
#     nta_name = Column(String, nullable=True)
#     nta_code = Column(String, nullable=True)
    
Base.metadata.create_all(bind=engine)