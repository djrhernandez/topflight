from src.graphql import db
from sqlalchemy import Column, Integer, String

class Hotel(db.Model):
    __tablename__ = "hotel"
    id = Column(Integer, primary_key=True)
    parid = Column(Integer, nullable=False)
    
    bbl = Column(Integer, nullable=True)
    bldg_class = Column(String(4), nullable=False)
    bldg_id_number = Column(Integer, nullable=True)
    block = Column(String, nullable=False)
    borocode = Column(Integer, nullable=False)
    borough = Column(String, nullable=True)
    census_tract = Column(Integer, nullable=True)
    community_board = Column(String(255), nullable=True)
    council_district = Column(String(255), nullable=True)
    latitude = Column(String(255), nullable=True)
    longitude = Column(String(255), nullable=True)
    lot = Column(Integer, nullable=False)
    nta_code = Column(String, nullable=True)
    nta_name = Column(String, nullable=True)
    owner_name = Column(String(255), nullable=False)
    postcode = Column(Integer, nullable=False)
    street_address = Column(String, nullable=True)
    tax_class = Column(String, nullable=False)
    tax_year = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Hotel id={self.id} | {self.parid} | {self.owner_name} | {self.bldg_class} | {self.borough}>"

    def to_dict(self):
        return {
            "id": self.id,
            "parid": self.parid,
            "bbl": self.bbl,
            "bldg_class": self.bldg_class,
            "bldg_id_number": self.bldg_id_number,
            "block": self.block,
            "borocode": self.borocode,
            "borough": self.borough,
            "census_tract": self.census_tract,
            "community_board": self.community_board,
            "council_district": self.council_district,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "lot": self.lot,
            "nta_code": self.nta_code,
            "nta_name": self.nta_name,
            "owner_name": self.owner_name,
            "postcode": self.postcode,
            "street_address": self.street_address,
            "tax_class": self.tax_class,
            "tax_year": self.tax_year
        }