import plotly.express as px
import pandas as pd

def generate_cost_distance_chart(route_details):
    df = pd.DataFrame(route_details, columns=[
        "From", "To", "Distance (KM)", "Estimated Time (Hours)", "Fuel Cost (INR)"
    ])
    fig = px.bar(df, x="To", y="Fuel Cost (INR)", color="From", title="Fuel Cost per Segment")
    return fig

def generate_distance_time_chart(route_details):
    df = pd.DataFrame(route_details, columns=[
        "From", "To", "Distance (KM)", "Estimated Time (Hours)", "Fuel Cost (INR)"
    ])
    fig = px.line(df, x="To", y="Estimated Time (Hours)", markers=True, title="Estimated Time per Segment")
    return fig
