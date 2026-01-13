# 🌦️ Event Weather Guard

**“Will It Rain During My Event?”**

Event Weather Guard is a backend service that analyzes **hourly weather forecasts** for outdoor events and determines whether the event is **Safe**, **Risky**, or **Unsafe** based on **deterministic and explainable rules**.
If the event is risky or unsafe, the service also recommends a **better time window within the next 24 hours**.

---

## 🚀 Features

* Accepts event details (location + time window)
* Fetches **hourly weather forecast** from Open-Meteo
* Applies **rule-based weather classification**
* Returns:

  * Event classification (Safe / Risky / Unsafe)
  * Severity score (0–100)
  * Clear explanation of triggered rules
  * Hour-by-hour forecast for the event window
  * Optional alternate time window recommendation
* No authentication
* No persistence (fully stateless)

---

## 🛠 Tech Stack

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **Open-Meteo API** (public & free)
* Async HTTP requests

---

## 📦 Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Pratham703/Weather_api_backend
cd Weather_forecast
```

### 2️⃣ Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI provides built-in documentation:

* **Swagger UI**
  👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

* **OpenAPI JSON**
  👉 [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

---

## 🔌 API Endpoint

### `POST /event-forecast`

Generates a weather advisory for a **single event**.

### Request Body

```json
{
  "name": "Football Match",
  "location": {
    "latitude": 10.79,
    "longitude": 79.86
  },
  "start_time": "2026-01-13T07:00:00",
  "end_time": "2026-01-13T09:00:00"
}
```

⏰ **Datetime format**
ISO-8601, 24-hour format (`YYYY-MM-DDTHH:MM:SS`)

---

### Example Response

```json
{
  "classification": "Risky",
  "severity_score": 37,
  "summary": "Rain probability is 80% at 07:00",
  "reason": [
    "Rain probability is 80% at 07:00"
  ],
  "event_window_forecast": [
    {
      "time": "07:00",
      "rain_prob": 80,
      "wind_kmh": 4.7,
      "precipitation_mm": 0.7
    }
  ],
  "recommended_alternate_window": {
    "start_time": "21:00",
    "end_time": "00:00",
    "reason": "Lower rain probability and calmer winds expected"
  }
}
```

---

## 🔄 Project Workflow

1. Client sends event details (location + time window)
2. Hourly forecast data is fetched from **Open-Meteo**
3. Forecast hours are filtered to match the event window
4. Weather rules are evaluated hour-by-hour
5. Severity score is calculated
6. Event is classified as Safe / Risky / Unsafe
7. If Risky or Unsafe, a better window is searched within the next 24 hours
8. A structured, explainable response is returned

---

## ⏱ Time-Window Forecast Handling

* Only forecast hours overlapping with the event window are considered
* Filtering logic:

```python
event.start_time <= forecast_hour < event.end_time
```

* Ensures accurate handling of short or partial-hour events

---

## 📏 Weather Classification Rules

### ❌ Unsafe

Triggered if **any hour** satisfies:

* Thunderstorm weather codes `{95, 96, 99}`
* Heavy rain (`precipitation_mm ≥ 5`)
* Extreme wind (`wind_speed > 40 km/h`)

### ⚠️ Risky

Triggered if **no Unsafe rules**, but any hour has:

* Rain probability ≥ 60%
* Moderate wind (`20–40 km/h`)
* Light to moderate precipitation

### ✅ Safe

* None of the above conditions apply across the event window

Worst-case condition dominates the final classification.

---

## 📊 Severity Score Logic (0–100)

Severity score provides a numeric representation of risk.

Weighted contributors:

* Rain probability
* Precipitation (mm)
* Wind speed (km/h)
* Thunderstorm presence (strong penalty)

Final score = **maximum severity across all event hours**

| Range  | Meaning |
| ------ | ------- |
| 0–20   | Safe    |
| 21–60  | Risky   |
| 61–100 | Unsafe  |

---

## 🔁 Alternate Time Recommendation Logic

Applied **only if event is Risky or Unsafe**.

Logic:

1. Scan hourly forecast for the **next 24 hours**
2. Apply same safety rules to each hour
3. Search for a **continuous block of safer hours**
4. Select the best available window based on:

   * Lower rain probability
   * Minimal precipitation
   * Calmer winds

If no suitable window exists:

```json
"recommended_alternate_window": null
```

---

## 🧪 Example curl Request (Optional)

```bash
curl -X POST http://127.0.0.1:8000/event-forecast \
-H "Content-Type: application/json" \
-d '{
  "name": "Football Match",
  "location": { "latitude": 10.79, "longitude": 79.86 },
  "start_time": "2026-01-13T07:00:00",
  "end_time": "2026-01-13T09:00:00"
}'
```

---

## ⚠️ Edge-Case Handling

* Invalid time window (`start_time >= end_time`)
* No forecast data for event window
* Incorrect datetime formats
* External API failures

All return appropriate HTTP error responses.

---

## 🔍 Key Assumptions & Trade-offs

* Uses Open-Meteo for free, reliable hourly data
* No database or persistence
* Forecast accuracy depends on external provider
* Recommendation limited to next 24 hours
* Conservative weather-code mapping for safety

---

## 📌 Status

✅ **Assignment Complete & Submission Ready**

