import streamlit as st
import requests
import folium

from datetime import datetime
from streamlit_folium import st_folium


st.title("🚕 TaxiFareModel")

st.write("Enter your ride information to estimate the fare and visualize the trip.")


# ---------------------------
# USER INPUTS
# ---------------------------

pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time")

pickup_longitude = st.number_input(
    "Pickup longitude",
    value=-73.950655,
    format="%.6f"
)

pickup_latitude = st.number_input(
    "Pickup latitude",
    value=40.783282,
    format="%.6f"
)

dropoff_longitude = st.number_input(
    "Dropoff longitude",
    value=-73.984365,
    format="%.6f"
)

dropoff_latitude = st.number_input(
    "Dropoff latitude",
    value=40.769802,
    format="%.6f"
)

passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    max_value=8,
    value=2
)


pickup_datetime = datetime.combine(
    pickup_date,
    pickup_time
).strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------
# TAXIFARE API
# ---------------------------

url = "https://taxifare.lewagon.ai/predict"

params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}


# ---------------------------
# ROUTE WITH OSRM
# ---------------------------

route_url = (
    f"https://router.project-osrm.org/route/v1/driving/"
    f"{pickup_longitude},{pickup_latitude};"
    f"{dropoff_longitude},{dropoff_latitude}"
    "?overview=full&geometries=geojson"
)

try:

    route_response = requests.get(
        route_url,
        timeout=10
    )

    route_data = route_response.json()

    route = route_data["routes"][0]

    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    coordinates = route["geometry"]["coordinates"]

    # Folium expects latitude, longitude
    route_points = [
        [lat, lon]
        for lon, lat in coordinates
    ]

except Exception:

    distance_km = None
    duration_min = None
    route_points = []


# ---------------------------
# MAP
# ---------------------------

center_lat = (pickup_latitude + dropoff_latitude) / 2
center_lon = (pickup_longitude + dropoff_longitude) / 2

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=13
)


folium.Marker(
    [pickup_latitude, pickup_longitude],
    tooltip="Pickup",
    popup="Pickup location",
    icon=folium.Icon(color="green")
).add_to(m)


folium.Marker(
    [dropoff_latitude, dropoff_longitude],
    tooltip="Dropoff",
    popup="Dropoff location",
    icon=folium.Icon(color="red")
).add_to(m)


if route_points:

    folium.PolyLine(
        route_points,
        weight=5,
        opacity=0.8
    ).add_to(m)


st.subheader("Trip")

st_folium(
    m,
    width=None,
    height=500
)


# ---------------------------
# TRIP INFORMATION
# ---------------------------

if distance_km is not None:

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Distance",
            f"{distance_km:.1f} km"
        )

    with col2:
        st.metric(
            "Estimated driving time",
            f"{duration_min:.0f} min"
        )


# ---------------------------
# PREDICTION
# ---------------------------

st.markdown("### Premium prediction")

st.write(
    "Unlock your TaxiFare prediction for **$199.99**."
)


if st.button("Unlock prediction — $199.99"):

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        prediction = response.json()["fare"]

        st.success(
            f"Estimated taxi fare: ${prediction:.2f}"
        )

    except Exception as e:

        st.error(
            f"Unable to retrieve prediction: {e}"
        )
