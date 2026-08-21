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
# REVOLUT-INSPIRED CSS
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background: #F5F5F7;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    h1, h2, h3, p, div, span, label {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* ---------- HEADER ---------- */

    .brand {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 3rem;
        color: #111111;
    }

    .hero-title {
        font-size: clamp(2.8rem, 6vw, 5rem);
        font-weight: 700;
        letter-spacing: -0.065em;
        line-height: 0.95;
        margin-bottom: 1rem;
        color: #090909;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #707070;
        max-width: 550px;
        margin-bottom: 2.5rem;
    }


    /* ---------- CARDS ---------- */

    .revolut-card {
        background: white;
        border-radius: 28px;
        padding: 28px;
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.04);
    }

    .dark-card {
        background: #0B0B0C;
        color: white;
        border-radius: 28px;
        padding: 30px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .section-label {
        color: #8A8A8E;
        font-size: 0.80rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }


    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: white;
        padding: 22px;
        border-radius: 22px;
        border: 1px solid rgba(0,0,0,0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #8A8A8E;
    }

    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 650;
        letter-spacing: -0.04em;
    }


    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] {
        border-radius: 16px;
        background: white;
    }

    div[data-baseweb="select"] {
        border-radius: 16px;
    }

    [data-testid="stNumberInput"] input {
        border-radius: 16px;
    }

    [data-testid="stDateInput"] input {
        border-radius: 16px;
    }


    /* ---------- BUTTON ---------- */

    div.stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 18px;
        border: none;
        background: #0B0B0C;
        color: white;
        font-size: 1rem;
        font-weight: 650;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #272729;
        color: white;
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: scale(0.99);
    }


    /* ---------- FOLIUM ---------- */

    iframe {
        border-radius: 26px !important;
    }


    /* ---------- PRICE ---------- */

    .price {
        font-size: 4rem;
        font-weight: 700;
        letter-spacing: -0.06em;
        line-height: 1;
        color: white;
        margin-top: 8px;
    }

    .price-description {
        color: #A1A1A6;
        margin-top: 10px;
    }


    /* ---------- SMALL TEXT ---------- */

    .muted {
        color: #8A8A8E;
        font-size: 0.9rem;
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
        Plan your journey, visualize your route and instantly estimate
        your taxi fare.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TRIP PARAMETERS
# =========================================================

st.markdown(
    '<div class="section-label">Your journey</div>',
    unsafe_allow_html=True
)

col_date, col_time, col_people = st.columns(3)

with col_date:

    pickup_date = st.date_input(
        "Date"
    )

with col_time:

    pickup_time = st.time_input(
        "Time"
    )

with col_people:

    passenger_count = st.number_input(
        "Passengers",
        min_value=1,
        max_value=8,
        value=2,
        step=1
    )


st.write("")


pickup_col, dropoff_col = st.columns(2)


# =========================================================
# PICKUP
# =========================================================

with pickup_col:

    st.markdown("### Pickup")

    pickup_longitude = st.number_input(
        "Longitude",
        value=-73.950655,
        format="%.6f",
        key="pickup_lon"
    )

    pickup_latitude = st.number_input(
        "Latitude",
        value=40.783282,
        format="%.6f",
        key="pickup_lat"
    )


# =========================================================
# DROPOFF
# =========================================================

with dropoff_col:

    st.markdown("### Destination")

    dropoff_longitude = st.number_input(
        "Longitude",
        value=-73.984365,
        format="%.6f",
        key="dropoff_lon"
    )

    dropoff_latitude = st.number_input(
        "Latitude",
        value=40.769802,
        format="%.6f",
        key="dropoff_lat"
    )


pickup_datetime = datetime.combine(
    pickup_date,
    pickup_time
).strftime("%Y-%m-%d %H:%M:%S")


# =========================================================
# ROUTING
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

    route_data = route_response.json()

    route = route_data["routes"][0]

    distance_km = route["distance"] / 1000
    duration_min = route["duration"] / 60

    coordinates = route["geometry"]["coordinates"]

    route_points = [
        [latitude, longitude]
        for longitude, latitude in coordinates
    ]

except Exception:

    st.warning("Route information is temporarily unavailable.")


# =========================================================
# JOURNEY SUMMARY
# =========================================================

st.write("")
st.markdown(
    '<div class="section-label">Trip overview</div>',
    unsafe_allow_html=True
)


metric1, metric2, metric3 = st.columns(3)


with metric1:

    if distance_km is not None:

        st.metric(
            "Distance",
            f"{distance_km:.1f} km"
        )

    else:

        st.metric(
            "Distance",
            "—"
        )


with metric2:

    if duration_min is not None:

        st.metric(
            "Travel time",
            f"{duration_min:.0f} min"
        )

    else:

        st.metric(
            "Travel time",
            "—"
        )


with metric3:

    st.metric(
        "Passengers",
        passenger_count
    )


# =========================================================
# MAP
# =========================================================

st.write("")

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


# Pickup marker
folium.CircleMarker(
    location=[
        pickup_latitude,
        pickup_longitude
    ],
    radius=9,
    color="#000000",
    fill=True,
    fill_color="#000000",
    fill_opacity=1,
    tooltip="Pickup"
).add_to(m)


# Destination marker
folium.CircleMarker(
    location=[
        dropoff_latitude,
        dropoff_longitude
    ],
    radius=9,
    color="#000000",
    fill=True,
    fill_color="#FFFFFF",
    fill_opacity=1,
    weight=3,
    tooltip="Destination"
).add_to(m)


# Route
if route_points:

    folium.PolyLine(
        route_points,
        color="#111111",
        weight=6,
        opacity=0.9
    ).add_to(m)

    m.fit_bounds(route_points)


st_folium(
    m,
    width=None,
    height=520,
    returned_objects=[]
)


# =========================================================
# TAXIFARE API
# =========================================================

url = "https://taxifare.lewagon.ai/predict"

params = {

    "pickup_datetime": pickup_datetime,

    "pickup_longitude":
        pickup_longitude,

    "pickup_latitude":
        pickup_latitude,

    "dropoff_longitude":
        dropoff_longitude,

    "dropoff_latitude":
        dropoff_latitude,

    "passenger_count":
        passenger_count
}


# =========================================================
# PREMIUM CARD
# =========================================================

st.markdown(
    """
    <div class="dark-card">

        <div style="
            color:#A1A1A6;
            font-size:0.8rem;
            font-weight:600;
            letter-spacing:0.08em;
            text-transform:uppercase;
        ">
            TaxiFare Premium
        </div>

        <div class="price">
            $199.99
        </div>

        <div class="price-description">
            Unlock your AI-powered fare prediction instantly.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PREDICTION
# =========================================================

if st.button(
    "Unlock fare prediction — $199.99",
    type="primary"
):

    with st.spinner(
        "Calculating your fare..."
    ):

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
                <div class="dark-card">

                    <div style="
                        color:#A1A1A6;
                        font-size:0.8rem;
                        text-transform:uppercase;
                        letter-spacing:0.08em;
                    ">
                        Estimated fare
                    </div>

                    <div class="price">
                        ${prediction:.2f}
                    </div>

                    <div class="price-description">
                        Estimated price for your selected journey.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        except requests.RequestException:

            st.error(
                "Unable to connect to the prediction service."
            )

        except (
            KeyError,
            TypeError,
            ValueError
        ):

            st.error(
                "The prediction service returned an unexpected response."
            )


# =========================================================
# FOOTER
# =========================================================

st.write("")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#9A9A9A;
        padding-top:40px;
        font-size:0.8rem;
    ">
        TaxiFare · AI-powered ride estimation
    </div>
    """,
    unsafe_allow_html=True
)
