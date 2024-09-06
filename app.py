from fastapi import FastAPI
import uvicorn
from map import MapRequest, MapResponse, find_spots
from booking import add_parking_spot, ParkingSpotBooking

app = FastAPI()

@app.post("/map/")
async def get_map_data(request: MapRequest) -> MapResponse:
    longitude = request.longitude
    latitude = request.latitude
    radius = request.radius
    
    return find_spots(latitude=latitude, longitude=longitude, radius=radius)

@app.post("/add_spot/")
async def new_parking_spot(request: ParkingSpotBooking) -> bool:
    return True if add_parking_spot(request) else False

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)