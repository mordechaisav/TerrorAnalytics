from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api_queries.postgres_db.models import Base


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    events = relationship('Event', back_populates='group')


