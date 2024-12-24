
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from load.postgres_db.models import Base


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    country = relationship('Country', back_populates='cities')
    events = relationship('Event', back_populates='city')