from sqlalchemy.orm import declarative_base

Base = declarative_base()

from api_queries.postgres_db.models.city_model import City
from api_queries.postgres_db.models.country_model import Country
from api_queries.postgres_db.models.event_model import Event
from api_queries.postgres_db.models.group_model import Group
from api_queries.postgres_db.models.region_model import Region
from api_queries.postgres_db.models.target_type_model import TargetType
from api_queries.postgres_db.models.attack_type_model import AttackType

