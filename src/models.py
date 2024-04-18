# models.py

import logging
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .utils import create_db_path

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

connection_str = create_db_path('skyhawk.db')

engine = create_engine(connection_str, echo=False)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

association_table = Table(
    "association",
    Base.metadata,
    Column("hotel_id", Integer, ForeignKey("hotels.parid")),
    Column("owner_id", Integer, ForeignKey("owners.id")),
)


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
    __tablename__ = "hotels"
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
    
    def full_address(self):
        return f"{self.street_num} {self.street_name}, {self.borough} {self.postcode}"

    def __repr__(self):
        return f"<Hotel {self.id}, {self.full_address()}>"


class Owners(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    hotels = relationship("Hotels", secondary=association_table, backref="owners")

    def __repr__(self):
        return f"<Owner {self.name} ({self.id})>"


Base.metadata.create_all(bind=engine)