def compare_vehicles(distance_km, fuel_price, vehicle_mileages, load_kg=None):
    results = {}
    for name, mileage in vehicle_mileages.items():
        adjusted_mileage = mileage
        if load_kg and load_kg > 500:
            adjusted_mileage *= 0.9  # reduce mileage by 10% for heavy loads
        litres = distance_km / adjusted_mileage
        cost = round(litres * fuel_price, 2)
        results[name] = {"Litres": round(litres, 2), "Cost": cost}
    return results
