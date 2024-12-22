from sqlalchemy import Integer, Column, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from api_queries.postgres_db.models import Base


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)
    day = Column(Integer, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    summary = Column(String, nullable=True)
    killed = Column(Integer)
    wounded = Column(Integer)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)
    attack_type_id = Column(Integer, ForeignKey('attack_types.id'), nullable=True)
    target_type_id = Column(Integer, ForeignKey('target_types.id'), nullable=True)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=True)
    group = relationship('Group', back_populates='events')
    attack_type = relationship('AttackType', back_populates='events')
    target_type = relationship('TargetType', back_populates='events')
    city = relationship('City', back_populates='events')