from sqlalchemy.orm import declarative_base

Base = declarative_base()

from api_queries.postgres_db.models.attack_type_model import AttackType
