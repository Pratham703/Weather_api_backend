THUNDER_CODES = {95, 96, 99}

def evaluate_weather_rules(forecast):
    reasons = []
    classification = "Safe"

    
    for hour in forecast:
        if hour["weathercode"] in THUNDER_CODES:
            return "Unsafe", ["Thunderstorm expected"]

        if hour["precipitation_mm"] >= 10:
            return "Unsafe", ["Heavy rain (>=10mm) detected"]

        if hour["wind_kmh"] >= 40:
            return "Unsafe", ["Very high wind speed (>=40 km/h)"]

    
    for hour in forecast:
        if hour["rain_prob"] >= 60:
            reasons.append(
                f"Rain probability is {hour['rain_prob']}% at {hour['time']}"
            )
            classification = "Risky"

        if 25 <= hour["wind_kmh"] < 40:
            reasons.append(
                f"Wind speed is {hour['wind_kmh']} km/h at {hour['time']}"
            )
            classification = "Risky"

    if classification == "Safe":
        reasons.append("No adverse weather conditions detected")

    return classification, reasons


def calculate_severity_score(forecast):
    max_score = 0

    for hour in forecast:
        score = 0
        score += min(40, hour["rain_prob"] * 0.4)
        score += min(30, hour["wind_kmh"] * 0.75)
        score += min(30, hour["precipitation_mm"] * 3)
        max_score = max(max_score, score)

    return min(100, int(max_score))
