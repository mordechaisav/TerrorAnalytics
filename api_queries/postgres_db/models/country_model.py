from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api_queries.postgres_db.models import Base


class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=True)
    region = relationship('Region', back_populates='countries')
    cities = relationship('City', back_populates='country')