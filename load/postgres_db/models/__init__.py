from sqlalchemy.orm import declarative_base

Base = declarative_base()

from load.postgres_db.models.city_model import City
from load.postgres_db.models.country_model import Country
from load.postgres_db.models.event_model import Event
from load.postgres_db.models.group_model import Group
from load.postgres_db.models.region_model import Region
from load.postgres_db.models.target_type_model import TargetType
from load.postgres_db.models.attack_type_model import AttackType

