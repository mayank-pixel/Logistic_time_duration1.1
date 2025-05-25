# final_app.py (Enhanced Traffic Prediction + Weight-Aware Pricing)

import streamlit as st
import pandas as pd
import joblib
from config import GOOGLE_API_KEY, OPENWEATHER_API_KEY
import googlemaps
from streamlit_folium import st_folium
import plotly.express as px

# Core logic modules
from core.distance_api import get_distance_km
from core.fuel_cost import calculate_fuel_cost
from core.traffic_delay import adjust_time_for_traffic
from core.weather import get_weather
from core.vehicle_compare import compare_vehicles
from core.report_export import generate_excel_report
from core.charts import generate_cost_distance_chart, generate_distance_time_chart
from core.timeline import generate_timeline
from core.map_renderer import render_map_with_stops
from core.session_manager import get_or_init_state

# Load model
model = joblib.load("models/route_time_predictor.pkl")
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

cities = ["Bengaluru", "Delhi", "Ahmedabad", "Visakhapatnam", "Mumbai", "Hyderabad", "Chennai", "Kolkata", "Pune", "Jaipur"]

city_coords = {
    "Bengaluru": (12.9716, 77.5946),
    "Delhi": (28.6139, 77.2090),
    "Ahmedabad": (23.0225, 72.5714),
    "Visakhapatnam": (17.6868, 83.2185),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873)
}

fuel_prices = {
    "Bengaluru": 97.0,
    "Delhi": 96.2,
    "Ahmedabad": 96.8,
    "Visakhapatnam": 99.0,
    "Mumbai": 106.3,
    "Hyderabad": 108.1,
    "Chennai": 102.4,
    "Kolkata": 106.5,
    "Pune": 105.0,
    "Jaipur": 109.2
}

vehicle_types = {
    "Mini Truck (10 km/l)": 10,
    "Medium Truck (6 km/l)": 6,
    "Heavy Truck (4 km/l)": 4
}

st.title("🚛 Smart Logistics Route Time & Cost Estimator")

vehicle_choice = st.selectbox("Select Vehicle Type", list(vehicle_types.keys()))
km_per_litre = vehicle_types[vehicle_choice]

load_weight = st.number_input("Enter Load Weight (kg)", min_value=0, value=500)
multi_stop = st.selectbox("Do you want Multi-Stop Route?", ["No", "Yes"])

if multi_stop == "No":
    from_city = st.selectbox("From City", cities, key="from1")
    to_city = st.selectbox("To City", cities, key="to1")
    stops = [from_city, to_city]
else:
    stops = st.multiselect("Select Cities in Route Order", cities, default=["Bengaluru", "Hyderabad", "Kolkata"])

if st.button("Predict Route") and len(stops) >= 2:
    route_details = []
    total_distance = 0
    total_time = 0
    total_cost = 0

    for i in range(len(stops) - 1):
        origin = stops[i]
        dest = stops[i + 1]
        try:
            distance = get_distance_km(origin, dest, GOOGLE_API_KEY)
            row = pd.DataFrame([[origin, dest, distance]], columns=["From", "To", "Distance (KM)"])
            base_time = model.predict(row)[0]
            weather = get_weather(origin, OPENWEATHER_API_KEY)

            # Adjust time dynamically based on weather severity and rush hour
            from datetime import datetime
            weather_risk_map = {
                "clear": 0.0,
                "sun": 0.0,
                "clouds": 0.10,
                "fog": 0.15,
                "rain": 0.20,
                "thunderstorm": 0.25
            }

            risk_factor = weather_risk_map.get(weather.lower(), 0.0)

            # Add rush hour delay
            current_hour = datetime.now().hour
            if 8 <= current_hour <= 10 or 17 <= current_hour <= 19:
                risk_factor += 0.10  # extra 10% delay, 0.0)
            adjusted_time = base_time * (1 + risk_factor)

            if risk_factor > 0:
                delay_percent = int(risk_factor * 100)
                badge = "🟢"
                if delay_percent >= 25:
                    badge = "🔴"
                elif delay_percent >= 10:
                    badge = "🟡"
                traffic_note = f"{badge} (↑ ~{delay_percent}% delay due to {weather} at {current_hour}:00 hrs)"
            else:
                traffic_note = f"(No major delays at {current_hour}:00 hrs)""(No major delays)"

            # Fuel cost with weight effect
            if load_weight > 500:
                km_per_litre *= 0.9

            fuel_rate = fuel_prices.get(origin, 100.0)
            litres_used, fuel_cost = calculate_fuel_cost(distance, fuel_rate, km_per_litre, load_kg=load_weight)

            route_details.append((origin, dest, distance, base_time, adjusted_time, fuel_cost, weather, traffic_note))
            total_distance += distance
            total_time += adjusted_time
            total_cost += fuel_cost

        except Exception as e:
            st.error(f"Error fetching {origin} to {dest}: {e}")

    st.session_state.route_ready = True
    st.session_state.route_details = route_details
    st.session_state.total_distance = total_distance
    st.session_state.total_time = total_time
    st.session_state.total_cost = total_cost
    st.session_state.stops = stops

if get_or_init_state("route_ready", False):
    st.subheader("📊 Route Summary")
    for origin, dest, dist, base_time, adjusted_time, cost, weather, traffic_note in st.session_state.route_details:
        st.write(f"**{origin} → {dest}**: {dist:.2f} km | Base Time: {base_time:.2f} hrs | Adjusted: {adjusted_time:.2f} hrs {traffic_note} | ₹{cost:.2f} | Weather: {weather}")

    st.success(f"Total Distance: **{st.session_state.total_distance:.2f} km**")
    st.success(f"Estimated Time (With Traffic): **{st.session_state.total_time:.2f} hrs**")
    st.success(f"Estimated Fuel Cost: ₹**{st.session_state.total_cost:.2f}**")

    m = render_map_with_stops(st.session_state.stops, city_coords)
    st_folium(m, width=700, height=300)

    df_report = generate_excel_report([(a, b, c, d, e) for a, b, c, d, e, f, g, h in st.session_state.route_details])
    st.download_button("📥 Download Route Report (Excel)", data=df_report, file_name="route_summary.xlsx")

    st.plotly_chart(generate_cost_distance_chart([(a, b, c, e, f) for a, b, c, d, e, f, _, _ in st.session_state.route_details]))
    st.plotly_chart(generate_distance_time_chart([(a, b, c, e, f) for a, b, c, d, e, f, _, _ in st.session_state.route_details]))
    st.plotly_chart(generate_timeline(st.session_state.route_details))

    # Vehicle Comparison
    st.subheader("🚛 Vehicle Type Comparison")
    comparison = compare_vehicles(
        distance_km=st.session_state.total_distance,
        fuel_price=fuel_prices.get(st.session_state.stops[0], 100.0),
        vehicle_mileages=vehicle_types,
        load_kg=load_weight
    )
    comp_df = pd.DataFrame([
        {"Vehicle": v, "Estimated Cost (₹)": data["Cost"], "Estimated Fuel (Litres)": data["Litres"]}
        for v, data in comparison.items()
    ])
    st.dataframe(comp_df.set_index("Vehicle"))

    # Vehicle Comparison Bar Chart
    st.plotly_chart(
        px.bar(
            comp_df,
            x="Vehicle",
            y="Estimated Cost (₹)",
            title="💰 Vehicle-wise Cost Comparison",
            color="Vehicle"
        )
    )
