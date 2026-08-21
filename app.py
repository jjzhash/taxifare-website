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

    :root {
        --bg: #F7F7F4;
        --card: #FFFFFF;
        --text: #151515;
        --muted: #7B7B76;
        --border: #E9E9E4;
        --accent: #D8FF45;
        --accent-soft: #F0FFC0;
        --dark: #171717;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(216,255,69,0.22),
                transparent 28%
            ),
            var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit default chrome */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Hero */
    .hero {
        background: var(--card);
        border-radius: 32px;
        border: 1px solid var(--border);
        padding: 40px;
        margin-bottom: 26px;
    }

    .hero-kicker {
        display: inline-block;
        background: var(--accent-soft);
        color: #384000;
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: clamp(3rem, 7vw, 5rem);
        font-weight: 760;
        letter-spacing: -0.065em;
        line-height: 0.95;
        color: var(--text);
        margin-bottom: 18px;
    }

    .hero-subtitle {
        max-width: 580px;
        color: var(--muted);
        font-size: 1.08rem;
        line-height: 1.55;
    }

    /* Section labels */
    .section-label {
        color: #81817B;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 1.4rem;
        margin-bottom: 0.8rem;
    }

    h1, h2, h3 {
        color: var(--text) !important;
    }

    h3 {
        font-size: 1.15rem !important;
        margin-bottom: 0.7rem !important;
    }

    label,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] p {
        color: #5E5E59 !important;
        font-weight: 550 !important;
    }

    /* Inputs */
    [data-baseweb="input"] {
        background: var(--card) !important;
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        min-height: 52px;
        box-shadow: none !important;
    }

    [data-baseweb="input"]:focus-within {
        border-color: #B2C82D !important;
        box-shadow: 0 0 0 3px rgba(216,255,69,0.20) !important;
    }

    [data-baseweb="input"] input {
        color: var(--text) !important;
        background: transparent !important;
    }

    [data-testid="stNumberInput"] button {
        color: var(--text) !important;
        background: var(--card) !important;
        border-color: var(--border) !important;
    }

    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input {
        color: var(--text) !important;
        background: var(--card) !important;
    }

    /* Predict button */
    div.stButton > button {
        width: 100%;
        min-height: 66px;
        border-radius: 18px;
        border: none;
        background: var(--accent);
        color: #171717;
        font-size: 1.06rem;
        font-weight: 750;
        margin-top: 8px;
        margin-bottom: 24px;
        transition: all 0.18s ease;
        box-shadow: 0 10px 28px rgba(130,150,20,0.18);
    }

    div.stButton > button:hover {
        background: #E1FF67;
        color: #111111;
        border: none;
        transform: translateY(-1px);
        box-shadow: 0 14px 34px rgba(130,150,20,0.24);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: var(--card);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid var(--border);
        min-height: 103px;
        margin-bottom: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: #85857E !important;
    }

    [data-testid="stMetricValue"] {
        color: var(--text) !important;
        font-size: 1.7rem !important;
        font-weight: 720 !important;
        letter-spacing: -0.04em;
    }

    /* Fare result */
    .fare-result {
        background: var(--dark);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 22px;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .fare-result:after {
        content: "";
        position: absolute;
        width: 180px;
        height: 180px;
        background: var(--accent);
        border-radius: 50%;
        right: -80px;
        top: -90px;
        opacity: 0.9;
    }

    .fare-label {
        color: #B6B6AF;
        font-size: 0.76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        position: relative;
        z-index: 1;
    }

    .fare-value {
        color: #FFFFFF;
        font-size: 3.2rem;
        font-weight: 760;
        letter-spacing: -0.055em;
        margin-top: 7px;
        position: relative;
        z-index: 1;
    }

    /* Map */
    iframe {
        border-radius: 24px !important;
        border: 1px solid var(--border) !important;
    }

    [data-testid="column"] {
        padding-left: 0.3rem;
        padding-right: 0.3rem;
    }

    .footer {
        text-align: center;
        color: #989890;
        padding-top: 42px;
        padding-bottom: 15px;
        font-size: 0.8rem;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1rem;
        }

        .hero {
            padding: 26px;
        }

        .hero-title {
            font-size: 3.15rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Smart ride estimate</div>
        <div class="hero-title">
            Know your fare<br>
            before you ride.
        </div>
        <div class="hero-subtitle">
            Enter your trip details, explore the route and get an instant
            AI-powered taxi fare estimate.
        </div>
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
# API
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
    route_response = requests.get(route_url, timeout=10)
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
# MINI GAME + PREDICTION
# =========================================================

import time
import random


if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "game_unlocked" not in st.session_state:
    st.session_state.game_unlocked = False

if "game_ready_at" not in st.session_state:
    st.session_state.game_ready_at = None


st.markdown(
    '<div class="section-label">Unlock your fare</div>',
    unsafe_allow_html=True
)


if not st.session_state.game_started and not st.session_state.game_unlocked:

    if st.button("Play to unlock prediction 🎮"):
        st.session_state.game_started = True
        st.session_state.game_ready_at = time.time() + random.uniform(2, 5)
        st.rerun()


elif st.session_state.game_started and not st.session_state.game_unlocked:

    st.info("Wait for the green signal, then click as fast as possible.")

    remaining = st.session_state.game_ready_at - time.time()

    if remaining > 0:

        st.warning("Not yet...")

        time.sleep(min(remaining, 1))
        st.rerun()

    else:

        start_time = time.time()

        st.success("GO!")

        if st.button("CLICK NOW! ⚡"):

            reaction_time = time.time() - start_time

            if reaction_time < 1.5:

                st.session_state.game_unlocked = True
                st.session_state.game_started = False

                st.success(
                    f"Unlocked! Reaction time: {reaction_time:.2f}s"
                )

                st.rerun()

            else:

                st.error(
                    f"Too slow: {reaction_time:.2f}s. Try again."
                )

                st.session_state.game_started = False
                st.session_state.game_ready_at = None

                st.rerun()


elif st.session_state.game_unlocked:

    st.success("Prediction unlocked")

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

    if st.button("Play again"):
        st.session_state.game_unlocked = False
        st.session_state.game_started = False
        st.session_state.game_ready_at = None
        st.rerun()

# =========================================================
# TRIP OVERVIEW + MAP
# =========================================================

st.markdown(
    '<div class="section-label">Trip overview</div>',
    unsafe_allow_html=True
)

overview_col, map_col = st.columns([1, 2], gap="large")

with overview_col:
    st.metric(
        "Distance",
        f"{distance_km:.1f} km" if distance_km is not None else "—"
    )

    st.metric(
        "Travel time",
        f"{duration_min:.0f} min" if duration_min is not None else "—"
    )

    st.metric("Passengers", passenger_count)

with map_col:
    center_lat = (pickup_latitude + dropoff_latitude) / 2
    center_lon = (pickup_longitude + dropoff_longitude) / 2

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles="CartoDB positron"
    )

    folium.CircleMarker(
        location=[pickup_latitude, pickup_longitude],
        radius=8,
        color="#171717",
        fill=True,
        fill_color="#D8FF45",
        fill_opacity=1,
        weight=3,
        tooltip="Pickup"
    ).add_to(m)

    folium.CircleMarker(
        location=[dropoff_latitude, dropoff_longitude],
        radius=8,
        color="#171717",
        fill=True,
        fill_color="#FFFFFF",
        fill_opacity=1,
        weight=3,
        tooltip="Destination"
    ).add_to(m)

    if route_points:
        folium.PolyLine(
            route_points,
            color="#171717",
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
    <div class="footer">
        AI-powered ride estimation
    </div>
    """,
    unsafe_allow_html=True
)
