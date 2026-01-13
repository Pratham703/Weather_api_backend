from fastapi import FastAPI, HTTPException
from dateutil.parser import isoparse
from datetime import timedelta
import logging

from .schemas import EventRequest, EventResponse
from .weather_client import fetch_weather
from .rules import evaluate_weather_rules, calculate_severity_score
from .recommender import recommend_alternate_window

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("event-weather-guard")

app = FastAPI(title="Event Weather Guard")


@app.get("/")
def health_check():
    return {"status": "Event Weather Guard is running"}


@app.post("/event-forecast", response_model=EventResponse)
async def event_forecast(event: EventRequest):
    logger.info("Request received | %s | %s -> %s", event.name, event.start_time, event.end_time)

    if event.start_time >= event.end_time:
        raise HTTPException(status_code=400, detail="start_time must be before end_time")

    weather_data = await fetch_weather(
        event.location.latitude,
        event.location.longitude
    )

    hourly = weather_data["hourly"]

    forecast_start = isoparse(hourly["time"][0])
    forecast_end = isoparse(hourly["time"][-1])

    if event.end_time < forecast_start or event.start_time > forecast_end:
        raise HTTPException(
            status_code=400,
            detail="Event time is outside the available weather forecast range"
        )

    event_window_forecast = []

    for i, t in enumerate(hourly["time"]):
        hour_time = isoparse(t)
        if event.start_time <= hour_time < event.end_time:
            event_window_forecast.append({
                "time": hour_time.strftime("%H:%M"),
                "rain_prob": hourly["precipitation_probability"][i],
                "wind_kmh": hourly["wind_speed_10m"][i],
                "precipitation_mm": hourly["precipitation"][i],
                "weathercode": hourly["weathercode"][i],
            })

    if not event_window_forecast:
        raise HTTPException(
            status_code=400,
            detail="No weather data available for event window"
        )

    classification, reasons = evaluate_weather_rules(event_window_forecast)
    severity_score = calculate_severity_score(event_window_forecast)

    logger.info("Classification=%s Severity=%s", classification, severity_score)

    recommendation_end_time = event.start_time + timedelta(hours=24)
    future_forecast = []

    for i, t in enumerate(hourly["time"]):
        hour_time = isoparse(t)
        if event.start_time <= hour_time <= recommendation_end_time:
            future_forecast.append({
                "time": hour_time,
                "rain_prob": hourly["precipitation_probability"][i],
                "wind_kmh": hourly["wind_speed_10m"][i],
                "precipitation_mm": hourly["precipitation"][i],
                "weathercode": hourly["weathercode"][i],
            })

    duration_hours = int(
        (event.end_time - event.start_time).total_seconds() / 3600
    )

    alternate_window = None
    if classification != "Safe":
        alternate_window = recommend_alternate_window(
            future_forecast,
            duration_hours
        )

    return {
        "classification": classification,
        "severity_score": severity_score,
        "summary": reasons[0],
        "reason": reasons,
        "event_window_forecast": [
            {
                "time": h["time"],
                "rain_prob": h["rain_prob"],
                "wind_kmh": h["wind_kmh"],
                "precipitation_mm": h["precipitation_mm"],
            }
            for h in event_window_forecast
        ],
        "recommended_alternate_window": alternate_window
    }
