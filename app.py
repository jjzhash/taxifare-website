import streamlit as st
import requests
from datetime import datetime


st.title("TaxiFareModel")

pickup_date = st.date_input("Pickup date")
pickup_time = st.time_input("Pickup time")

pickup_longitude = st.number_input(
    "Pickup longitude",
    value=-73.950655
)

pickup_latitude = st.number_input(
    "Pickup latitude",
    value=40.783282
)

dropoff_longitude = st.number_input(
    "Dropoff longitude",
    value=-73.984365
)

dropoff_latitude = st.number_input(
    "Dropoff latitude",
    value=40.769802
)

passenger_count = st.number_input(
    "Passenger count",
    min_value=1,
    value=2
)

pickup_datetime = datetime.combine(
    pickup_date,
    pickup_time
).strftime("%Y-%m-%d %H:%M:%S")


url = "https://taxifare.lewagon.ai/predict"

params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count,
}


if st.button("Predict"):

    response = requests.get(
        url,
        params=params
    )

    prediction = response.json()["fare"]

    st.success(
        f"Estimated fare: ${prediction:.2f}"
    )
