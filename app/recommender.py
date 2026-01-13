from datetime import timedelta
from .rules import evaluate_weather_rules, calculate_severity_score


def recommend_alternate_window(hourly_data, duration_hours):
    """
    Recommends the safest alternate time window of the same duration
    within the next 24 hours.
    """

    if len(hourly_data) < duration_hours:
        return None

    best_window = None
    best_score = float("inf")

    for i in range(len(hourly_data) - duration_hours + 1):
        window = hourly_data[i:i + duration_hours]

        classification, _ = evaluate_weather_rules(window)

        if classification != "Safe":
            continue

        score = calculate_severity_score(window)

        if score < best_score:
            best_score = score
            best_window = window

    if not best_window:
        return None

    start_time = best_window[0]["time"]
    end_time = start_time + timedelta(hours=duration_hours)

    return {
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
        "reason": "Lower rain probability and calmer winds expected"
    }
