from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a postgressql engine instance
engine = create_engine('postgresql+psycopg2://postgres:Iam$hreeraj04@localhost/vector')

# Create a DeclarativeMeta instance
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
