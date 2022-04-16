from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float

# Create a postgressql engine instance
engine = create_engine('postgresql+psycopg2://postgres:Iam$hreeraj04@localhost/vector')

# Create a DeclarativeMeta instance
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Define To Do class inheriting from Base
class Geography(Base):
    __tablename__ = "geography"
    id = Column(Integer, primary_key=True)
    continent_name = Column(String(50))
    country_name = Column(String(50))
    city_name = Column(String(50))
    continent_population = Column(Integer)
    city_population = Column(Integer)
    continent_area = Column(Float)
    country_area = Column(Float)
    city_area = Column(Float)
    city_num_roads = Column(Integer)
    city_num_trees = Column(Integer)
    country_num_hospitals = Column(Integer)
    country_num_parks = Column(Integer)

