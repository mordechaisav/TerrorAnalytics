from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from api_queries.postgres_db.models import Base


class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    countries = relationship('Country', back_populates='region')