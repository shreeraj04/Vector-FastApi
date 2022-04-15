from pydantic import BaseModel
from typing import Optional

# Create GeographyCreate Schema (Pydantic Model)
class GeographyCreate(BaseModel):
    continent_name: str
    country_name: str
    city_name: str
    continent_population: int
    city_population: int
    continent_area: float
    country_area: float
    city_area: float
    city_num_roads: float
    city_num_trees: int
    country_num_hospitals: int
    country_num_parks: int

# Create GeographyUpdate Schema (Pydantic Model)
class GeographyUpdate(BaseModel):
    continent_population: Optional[int]
    city_population: Optional[int]
    city_num_roads: Optional[float]
    city_num_trees: Optional[int]
    country_num_hospitals: Optional[int]
    country_num_parks: Optional[int]


# Complete Geography Schema (Pydantic Model)
class Geography(BaseModel):
    # id: int
    continent_name: str

    class Config:
        orm_mode: True
