import httpx

async def fetch_weather(latitude: float, longitude: float):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}&longitude={longitude}"
        "&hourly=precipitation_probability,precipitation,"
        "wind_speed_10m,weathercode"
        "&timezone=auto"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
