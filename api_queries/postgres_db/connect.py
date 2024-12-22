from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api_queries.postgres_db.models import Base
DB_URL = "postgresql://postgres:1234@127.0.0.1:5433/terror_db"

engine = create_engine(DB_URL)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
