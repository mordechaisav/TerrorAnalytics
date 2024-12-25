from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from load.postgres_db.models import Base


class AttackType(Base):
    __tablename__ = 'attack_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    events = relationship('Event', back_populates='attack_type')
