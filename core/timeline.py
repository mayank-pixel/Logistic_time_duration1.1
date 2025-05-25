import plotly.figure_factory as ff

def generate_timeline(route_details):
    """
    Generate a Gantt-style timeline chart using route details.
    """
    tasks = []
    start_time = 0

    for i, (from_city, to_city, dist, base_time, adjusted_time, cost, weather, note) in enumerate(route_details):
        end_time = start_time + adjusted_time
        tasks.append({
            "Task": f"{from_city} → {to_city}",
            "Start": start_time,
            "Finish": end_time
        })
        start_time = end_time

    fig = ff.create_gantt(tasks, index_col='Task', title="Estimated Route Timeline (in Hours)", show_colorbar=True, bar_width=0.3)
    return fig
