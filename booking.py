from postgres import PostgresDB
from pydantic import BaseModel

class ParkingSpotBooking(BaseModel):
    name: str
    email: str
    latitude: float
    longitude: float
    days_available: int
    price: float
    address: str
    underground: bool

def add_parking_spot(info: ParkingSpotBooking):
    table = "parking_spots"
    columns = ["name", "latitude", "longitude", "days_available"]  # add support for other fields in table then add here
    values = [info.name, info.email, info.latitude, info.longitude, info.days_available]
    pgcx = PostgresDB()
    pgcx.insert_data(table=table, coluns=columns, values=values)