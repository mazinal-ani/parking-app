from pydantic import BaseModel
import math
from typing import List
from postgres import PostgresDB

class MapRequest(BaseModel):
    longitude: float
    latitude: float
    radius: float

class ParkingSpotMap(BaseModel):
    account: str
    longitude: float
    latitude: float
    days_available: int
    price: float

class MapResponse(BaseModel):
    spots: List[ParkingSpotMap]

def get_bounding_box(latitude_in_degrees, longitude_in_degrees, radius_km):
    lat = math.radians(latitude_in_degrees)
    lon = math.radians(longitude_in_degrees)

    radius  = 6371
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - radius_km/radius
    lat_max = lat + radius_km/radius
    lon_min = lon - radius_km/parallel_radius
    lon_max = lon + radius_km/parallel_radius
    rad2deg = math.degrees

    lat_min = rad2deg(lat_min)
    lon_min = rad2deg(lon_min)
    lat_max = rad2deg(lat_max)
    lon_max = rad2deg(lon_max)

    return lat_min, lon_min, lat_max, lon_max

def find_spots(longitude: float, latitude: float, radius: float):
    lat_min, lon_min, lat_max, lon_max = get_bounding_box(longitude_in_degrees=longitude, latitude_in_degrees=latitude, radius_km=radius)
    pgcx = PostgresDB()
    pgcx.connect()

    # we gotta fix this later to make it safe from SQL injection
    query = f"""
    SELECT * FROM parking_spots ps WHERE latitude > {lat_min} AND longitude > {lon_min} AND latitude < {lat_max} AND longitude < {lon_max}
    """
    result = pgcx.select_data(query)

    pgcx.close() # we should probably make a destructor that closes this once it goes out of scope so we don't have to keep opening and closing manually

    resulting_spots = []
    
    for entry in result:
        resulting_spots.append(
            ParkingSpotMap(
                account=entry[0],
                longitude=entry[3],
                latitude=entry[2],
                days_available=entry[4],
                price=100  # default for now
            )
        )
    
    return MapResponse(spots=resulting_spots)
