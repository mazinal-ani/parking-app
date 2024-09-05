from fastapi import FastAPI
import uvicorn
from map import MapRequest, MapResponse, find_spots

app = FastAPI()

@app.post("/map/")
async def get_map_data(request: MapRequest) -> MapResponse:
    account = request.account
    longitude = request.longitude
    latitude = request.latitude
    radius = request.radius
    
    return find_spots(latitude=latitude, longitude=longitude, radius=radius)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)