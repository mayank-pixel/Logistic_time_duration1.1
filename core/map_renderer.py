import folium

def render_map_with_stops(stops, city_coords):
    m = folium.Map(location=city_coords[stops[0]], zoom_start=5)
    for city in stops:
        if city in city_coords:
            folium.Marker(city_coords[city], tooltip=city).add_to(m)
    for i in range(len(stops) - 1):
        loc1 = city_coords.get(stops[i])
        loc2 = city_coords.get(stops[i + 1])
        if loc1 and loc2:
            folium.PolyLine([loc1, loc2], color="blue", weight=4).add_to(m)
    return m
