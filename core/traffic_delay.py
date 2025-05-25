from datetime import datetime

def adjust_time_for_traffic(original_time, hour=None):
    if hour is None:
        hour = datetime.now().hour
    if 8 <= hour <= 10 or 17 <= hour <= 19:
        return round(original_time * 1.15, 2)
    return original_time
