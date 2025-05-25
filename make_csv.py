import googlemaps
import pandas as pd
import time
import os
from config import GOOGLE_API_KEY

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

# List of major Indian cities
cities = [
    "Bengaluru", "Delhi", "Ahmedabad", "Visakhapatnam",
    "Kolkata", "Mumbai", "Hyderabad", "Chennai", "Pune", "Jaipur"
]

# Prepare data list
data = []

# Create combinations and fetch distances
for origin in cities:
    for destination in cities:
        if origin != destination:
            try:
                result = gmaps.distance_matrix(origins=origin, destinations=destination, mode="driving")
                element = result["rows"][0]["elements"][0]

                distance_km = element["distance"]["value"] / 1000  # meters to km
                duration_hr = element["duration"]["value"] / 3600  # seconds to hours
                fuel_cost = round(distance_km * 8, 2)  # simple estimation: ₹8/km

                data.append([origin, destination, round(distance_km, 2), round(duration_hr, 2), fuel_cost])
                print(f"{origin} → {destination}: {distance_km:.2f} km, {duration_hr:.2f} hrs")

                time.sleep(1)  # to avoid hitting rate limits
            except Exception as e:
                print(f"Error fetching {origin} → {destination}: {e}")

# Create DataFrame
df = pd.DataFrame(data, columns=["From", "To", "Distance (KM)", "Time (Hours)", "Fuel Cost (₹)"])

# Ensure /data directory exists
os.makedirs("data", exist_ok=True)

# Save to CSV
df.to_csv("data/real_india_city_routes.csv", index=False)
print("✅ Saved as data/real_india_city_routes.csv")
