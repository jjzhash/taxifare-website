import streamlit as st
import requests
import folium

from datetime import datetime
from streamlit_folium import st_folium


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TaxiFare",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #F4F4F6;
        color: #111111;
    }

    .block-container {
        max-width: 1080px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .brand {
        font-size: 1.1rem;
        font-weight: 700;
        color: #111111;
        margin-bottom: 3rem;
    }

    .hero-title {
        font-size: clamp(3rem, 7vw, 5.2rem);
        font-weight: 750;
        letter-spacing: -0.065em;
        line-height: 0.93;
        color: #050505;
        margin-bottom: 1.4rem;
    }

    .hero-subtitle {
        font-size: 1.12rem;
        color: #66666B;
        max-width: 560px;
        line-height: 1.5;
        margin-bottom: 3rem;
    }

    .section-label {
        color: #6D6D73;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    h1, h2, h3 {
        color: #111111 !important;
    }

    h3 {
        font-size: 1.3rem !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.8rem !important;
    }

    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #55555A !important;
        font-weight: 500 !important;
    }

    [data-baseweb="input"] {
        background: #FFFFFF !important;
        border-radius: 16px !important;
        border: 1px solid #E2E2E6 !important;
        min-height: 52px;
    }

    [data-baseweb="input"] input {
        color: #111111 !important;
        background: transparent !important;
    }

    [data-testid="stNumberInput"] button {
        color: #111111 !important;
        background: #FFFFFF !important;
        border-color: #E2E2E6 !important;
    }

    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input {
        color: #111111 !important;
        background: #FFFFFF !important;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        padding: 22px;
        border-radius: 22px;
        border: 1px solid #E7E7EA;
        min-height: 105px;
        margin-bottom: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #717178 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111111 !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.04em;
    }

    div.stButton > button {
        width: 100%;
        min-height: 64px;
        border-radius: 20px;
        border: none;
        background: #111111;
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 10px;
        margin-bottom: 24px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #2A2A2D;
        color: #FFFFFF;
        transform: translateY(-1px);
        border: none;
    }

    div.stButton > button:active {
        transform: scale(0.99);
    }

    iframe {
        border-radius: 28px !important;
        border: 1px solid #E7E7EA !important;
    }

    [data-testid="column"] {
        padding-left: 0.35rem;
        padding-right: 0.35rem;
    }

    .fare-result {
        background: #111111;
        color: white;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .fare-label {
        color: #A7A7AD;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .fare-value {
        color: #FFFFFF;
        font-size: 3.2rem;
        font-weight: 750;
        letter-spacing: -0.05em;
        margin-top: 6px;
    }

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1.1rem;
            padding-right: 1.1rem;
        }

        .hero-title {
            font-size: 3.3rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="brand">TaxiFare</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-title">
        Your ride.<br>
        Your price.
    </div>

    <div class="hero-subtitle">
        Plan your journey, visualize your route and instantly estimate your taxi fare.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# JOURNEY
# =========================================================

st.markdown(
    '<div class="section-label">Your journey</div>',
    unsafe_allow_html=True
)

col_date, col_time, col_people = st.columns(3)

with col_date:
    pickup_date = st.date_input("Date")

with col_time:
    pickup_time = st.time_input("Time")

with col_people:
    passenger_count = st.number_input(
        "Passengers",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )


st.write("")


# =========================================================
# LOCATIONS
# =========================================================

pickup_col, dropoff_col = st.columns(2)

with pickup_col:

    st.subheader("Pickup")

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


with dropoff_col:

    st.subheader("Destination")

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


pickup_datetime = datetime.combine(
    pickup_date,
    pickup_time
).strftime("%Y-%m-%d %H:%M:%S")


# =========================================================
# API PARAMS
# =========================================================

url = "https://taxifare.lewagon.ai/predict"

params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}


# =========================================================
# ROUTE
# =========================================================

route_url = (
    "https://router.project-osrm.org/route/v1/driving/"
    f"{pickup_longitude},{pickup_latitude};"
    f"{dropoff_longitude},{dropoff_latitude}"
    "?overview=full&geometries=geojson"
)

distance_km = None
duration_min = None
route_points = []

try:

    route_response = requests.get(
        route_url,
        timeout=10
    )

    route_response.raise_for_status()

    route = route_response.json()["routes"][0]

    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    route_points = [
        [lat, lon]
        for lon, lat in route["geometry"]["coordinates"]
    ]

except Exception:
    pass


# =========================================================
# PREDICTION BUTTON
# =========================================================

st.markdown(
    '<div class="section-label">Fare prediction</div>',
    unsafe_allow_html=True
)

if st.button(
    "Unlock fare prediction — $199.99",
    type="primary"
):

    with st.spinner("Calculating your fare..."):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            prediction = float(
                response.json()["fare"]
            )

            st.markdown(
                f"""
                <div class="fare-result">

                    <div class="fare-label">
                        Estimated fare
                    </div>

                    <div class="fare-value">
                        ${prediction:.2f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception:

            st.error(
                "Unable to retrieve the fare prediction."
            )


# =========================================================
# TRIP OVERVIEW + MAP
# =========================================================

st.markdown(
    '<div class="section-label">Trip overview</div>',
    unsafe_allow_html=True
)

overview_col, map_col = st.columns(
    [1, 2],
    gap="large"
)


# -------------------------
# LEFT : METRICS
# -------------------------

with overview_col:

    st.metric(
        "Distance",
        f"{distance_km:.1f} km"
        if distance_km is not None
        else "—"
    )

    st.metric(
        "Travel time",
        f"{duration_min:.0f} min"
        if duration_min is not None
        else "—"
    )

    st.metric(
        "Passengers",
        passenger_count
    )


# -------------------------
# RIGHT : MAP
# -------------------------

with map_col:

    center_lat = (
        pickup_latitude + dropoff_latitude
    ) / 2

    center_lon = (
        pickup_longitude + dropoff_longitude
    ) / 2


    m = folium.Map(
        location=[
            center_lat,
            center_lon
        ],
        zoom_start=13,
        tiles="CartoDB positron"
    )


    folium.CircleMarker(
        location=[
            pickup_latitude,
            pickup_longitude
        ],
        radius=8,
        color="#111111",
        fill=True,
        fill_color="#111111",
        fill_opacity=1,
        tooltip="Pickup"
    ).add_to(m)


    folium.CircleMarker(
        location=[
            dropoff_latitude,
            dropoff_longitude
        ],
        radius=8,
        color="#111111",
        fill=True,
        fill_color="#FFFFFF",
        fill_opacity=1,
        weight=3,
        tooltip="Destination"
    ).add_to(m)


    if route_points:

        folium.PolyLine(
            route_points,
            color="#111111",
            weight=5,
            opacity=0.9
        ).add_to(m)

        m.fit_bounds(route_points)


    st_folium(
        m,
        width=None,
        height=380,
        returned_objects=[]
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#88888E;
        padding-top:50px;
        padding-bottom:20px;
        font-size:0.8rem;
    ">
        TaxiFare · AI-powered ride estimation
    </div>
    """,
    unsafe_allow_html=True
)
