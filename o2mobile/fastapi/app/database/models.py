from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from app.database.connection import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # PostGIS geometry column (Point, 4326 = WGS84)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
