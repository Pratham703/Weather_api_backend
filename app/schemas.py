from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Location(BaseModel):
    latitude: float
    longitude: float

class EventRequest(BaseModel):
    name: str
    location: Location
    start_time: datetime
    end_time: datetime

class HourlyForecast(BaseModel):
    time: str
    rain_prob: int
    wind_kmh: float
    precipitation_mm: float

class EventResponse(BaseModel):
    classification: str
    severity_score: int
    summary: str
    reason: List[str]
    event_window_forecast: List[HourlyForecast]
    recommended_alternate_window: Optional[dict]
