from sqlalchemy import Column, Integer, String, Float
from database import Base

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

class Continent(Base):
    __tablename__ = "continent"
    id = Column(Integer, primary_key=True)
    continent_name = Column(String(50))
    total_continent_population = Column(Integer)

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    city_name = Column(String(50))
    total_city_population = Column(Integer)