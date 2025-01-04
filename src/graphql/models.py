from src.graphql import db
from sqlalchemy import Column, Integer, String

class Hotel(db.Model):
    __tablename__ = "hotel"
    id = Column(Integer, primary_key=True)
    parid = Column(Integer, nullable=False)
    
    bldg_id_number = Column(Integer, nullable=False)
    bbl = Column(Integer, nullable=False)
    bldg_class = Column(String(4), nullable=False)
    block = Column(String, nullable=False)
    borocode = Column(Integer, nullable=False)
    borough = Column(String, nullable=False)
    census_tract = Column(Integer, nullable=False)
    community_board = Column(String(255), nullable=False)
    council_district = Column(String(255), nullable=False)
    latitude = Column(String(255), nullable=False)
    longitude = Column(String(255), nullable=False)
    lot = Column(Integer, nullable=False)
    nta = Column(String, nullable=False)
    owner_name = Column(String(255), nullable=False)
    postcode = Column(Integer, nullable=False)
    street_address = Column(String, nullable=False)
    tax_class = Column(String, nullable=False)
    tax_year = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Hotel id={self.id} | {self.parid} | {self.owner_name} | {self.bldg_class} | {self.borough}>"

    def to_dict(self):
        return {
            "id": self.id,
            "parid": self.parid,
            "bldg_id_number": self.bldg_id_number,
            "bbl": self.bbl,
            "bldg_class": self.bldg_class,
            "block": self.block,
            "borocode": self.borocode,
            "borough": self.borough,
            "census_tract": self.census_tract,
            "community_board": self.community_board,
            "council_district": self.council_district,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "lot": self.lot,
            "nta": self.nta,
            "owner_name": self.owner_name,
            "postcode": self.postcode,
            "street_address": self.street_address,
            "tax_class": self.tax_class,
            "tax_year": self.tax_year
        }