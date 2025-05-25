import googlemaps

def get_distance_km(origin, destination, api_key):
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.distance_matrix(origins=origin, destinations=destination, mode="driving")
    distance_m = result["rows"][0]["elements"][0]["distance"]["value"]
    return round(distance_m / 1000, 2)
