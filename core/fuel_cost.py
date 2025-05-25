def calculate_fuel_cost(distance_km, fuel_price, mileage_kmpl, load_kg=None):
    """
    Estimate fuel cost for a route segment.

    Parameters:
        distance_km (float): Distance of the segment in kilometers
        fuel_price (float): City-specific fuel price (INR per litre)
        mileage_kmpl (float): Vehicle mileage (km per litre)
        load_kg (float, optional): Load weight; reduces mileage if > 500kg

    Returns:
        litres (float): Litres consumed
        cost (float): INR cost of fuel
    """
    mileage = mileage_kmpl

    # Adjust mileage if weight is heavy
    if load_kg and load_kg > 500:
        mileage *= 0.9  # reduce mileage by 10%

    litres = distance_km / mileage
    cost = round(fuel_price * litres, 2)

    return round(litres, 2), cost
