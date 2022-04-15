from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a sqlite engine instance
engine = create_engine("sqlite:///geography.db")

# Create a DeclarativeMeta instance
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
