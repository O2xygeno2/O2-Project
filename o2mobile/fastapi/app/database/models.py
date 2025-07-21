from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from app.database.connection import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
    properties = Column(JSONB)
