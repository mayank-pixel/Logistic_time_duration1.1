import pandas as pd
from io import BytesIO

def generate_excel_report(route_details):
    """
    Converts route details into an Excel file in-memory.
    Returns a BytesIO stream for download.
    """
    df = pd.DataFrame(route_details, columns=[
        "From", "To", "Distance (KM)", "Estimated Time (Hours)", "Fuel Cost (INR)"
    ])

    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Route Summary')
        writer.close()

    buffer.seek(0)
    return buffer
