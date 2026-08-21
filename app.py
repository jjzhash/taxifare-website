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
# SNAKE GAME + AUTO UNLOCK + LEADERBOARD
# =========================================================

import json
import streamlit.components.v1 as components


st.markdown(
    '<div class="section-label">Unlock your fare</div>',
    unsafe_allow_html=True
)


# Parameters passed from Streamlit to JavaScript
game_params = json.dumps({
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
})


snake_html = f"""
<div id="game-app">

    <style>

        * {{
            box-sizing: border-box;
        }}

        #game-app {{
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;

            color: #171717;
            width: 100%;
        }}

        .game-layout {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
        }}

        .game-card {{
            background: #FFFFFF;
            border: 1px solid #E9E9E4;
            border-radius: 24px;
            padding: 22px;
        }}

        .game-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}

        .game-title {{
            font-size: 20px;
            font-weight: 750;
            letter-spacing: -0.03em;
        }}

        .game-subtitle {{
            font-size: 13px;
            color: #81817B;
            margin-top: 4px;
        }}

        .score-pill {{
            background: #F0FFC0;
            border-radius: 999px;
            padding: 8px 14px;
            font-weight: 750;
            font-size: 14px;
        }}

        canvas {{
            display: block;
            width: 100%;
            height: auto;

            background: #171717;

            border-radius: 20px;
            outline: none;
        }}

        .game-message {{
            min-height: 24px;
            margin-top: 14px;

            color: #777770;
            font-size: 14px;
        }}

        .restart-button {{
            width: 100%;
            height: 50px;

            margin-top: 12px;

            border: none;
            border-radius: 16px;

            background: #D8FF45;
            color: #171717;

            font-weight: 750;
            font-size: 14px;

            cursor: pointer;
        }}

        .restart-button:hover {{
            background: #E2FF6E;
        }}

        .leaderboard-title {{
            font-size: 16px;
            font-weight: 750;
            margin-bottom: 14px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            text-align: left;
            color: #8B8B84;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding-bottom: 10px;
        }}

        td {{
            padding: 11px 0;
            border-top: 1px solid #EEEEEA;
            font-size: 14px;
        }}

        .rank {{
            width: 40px;
            font-weight: 700;
        }}

        .leader-score {{
            font-weight: 750;
            text-align: right;
        }}

        .unlock-card {{
            margin-top: 20px;

            background: #171717;
            color: white;

            border-radius: 24px;
            padding: 24px;

            display: none;

            position: relative;
            overflow: hidden;
        }}

        .unlock-card::after {{
            content: "";

            position: absolute;

            width: 150px;
            height: 150px;

            right: -60px;
            top: -70px;

            background: #D8FF45;
            border-radius: 50%;
        }}

        .unlock-label {{
            color: #AFAFA8;

            font-size: 11px;
            font-weight: 700;

            letter-spacing: 0.08em;
            text-transform: uppercase;

            position: relative;
            z-index: 2;
        }}

        .unlock-price {{
            font-size: 46px;
            font-weight: 800;

            letter-spacing: -0.06em;

            margin-top: 6px;

            position: relative;
            z-index: 2;
        }}

        .unlock-text {{
            color: #BDBDB7;
            font-size: 14px;

            margin-top: 8px;

            position: relative;
            z-index: 2;
        }}

        @media (max-width: 700px) {{

            .game-layout {{
                grid-template-columns: 1fr;
            }}

        }}

    </style>


    <div class="game-layout">


        <!-- GAME -->
        <div class="game-card">

            <div class="game-header">

                <div>
                    <div class="game-title">
                        Snake Challenge
                    </div>

                    <div class="game-subtitle">
                        Get 2 points to unlock your fare.
                    </div>
                </div>

                <div class="score-pill">
                    Score:
                    <span id="score">
                        0
                    </span>
                </div>

            </div>


            <canvas
                id="snakeCanvas"
                width="620"
                height="360"
                tabindex="0">
            </canvas>


            <div
                id="message"
                class="game-message">

                Click the game and use your arrow keys.

            </div>


            <button
                id="restart"
                class="restart-button">

                Restart game

            </button>

        </div>


        <!-- LEADERBOARD -->
        <div class="game-card">

            <div class="leaderboard-title">
                Leaderboard
            </div>


            <table>

                <thead>

                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th style="text-align:right;">
                            Score
                        </th>
                    </tr>

                </thead>


                <tbody id="leaderboard">

                    <tr>
                        <td class="rank">1</td>
                        <td>Snake King</td>
                        <td class="leader-score">12</td>
                    </tr>

                    <tr>
                        <td class="rank">2</td>
                        <td>Taxi Racer</td>
                        <td class="leader-score">8</td>
                    </tr>

                    <tr>
                        <td class="rank">3</td>
                        <td>NYC Driver</td>
                        <td class="leader-score">5</td>
                    </tr>

                    <tr>
                        <td class="rank">4</td>
                        <td>You</td>
                        <td
                            id="player-score"
                            class="leader-score">
                            0
                        </td>
                    </tr>

                </tbody>

            </table>


            <div
                id="unlock-card"
                class="unlock-card">

                <div class="unlock-label">
                    Fare unlocked
                </div>

                <div
                    id="prediction"
                    class="unlock-price">

                    ...

                </div>

                <div class="unlock-text">
                    AI-powered estimated fare
                </div>

            </div>

        </div>

    </div>

</div>


<script>

    // =====================================================
    // CONFIG
    // =====================================================

    const API_URL =
        "https://taxifare.lewagon.ai/predict";

    const API_PARAMS =
        {game_params};

    const TARGET_SCORE = 2;


    // =====================================================
    // ELEMENTS
    // =====================================================

    const canvas =
        document.getElementById("snakeCanvas");

    const ctx =
        canvas.getContext("2d");

    const scoreElement =
        document.getElementById("score");

    const playerScoreElement =
        document.getElementById("player-score");

    const messageElement =
        document.getElementById("message");

    const restartButton =
        document.getElementById("restart");

    const unlockCard =
        document.getElementById("unlock-card");

    const predictionElement =
        document.getElementById("prediction");


    // =====================================================
    // GAME CONFIG
    // =====================================================

    const grid = 20;

    const cols =
        canvas.width / grid;

    const rows =
        canvas.height / grid;


    let snake = [];

    let food;

    let dx = 1;
    let dy = 0;

    let nextDx = 1;
    let nextDy = 0;

    let score = 0;

    let interval = null;

    let predictionUnlocked = false;


    // =====================================================
    // RANDOM FOOD
    // =====================================================

    function createFood() {{

        let position;

        do {{

            position = {{

                x:
                    Math.floor(
                        Math.random() * cols
                    ),

                y:
                    Math.floor(
                        Math.random() * rows
                    )

            }};

        }} while (

            snake.some(
                part =>
                    part.x === position.x &&
                    part.y === position.y
            )

        );


        return position;

    }}


    // =====================================================
    // RESET
    // =====================================================

    function resetGame() {{

        snake = [

            {{x: 8, y: 8}},
            {{x: 7, y: 8}},
            {{x: 6, y: 8}}

        ];


        dx = 1;
        dy = 0;

        nextDx = 1;
        nextDy = 0;

        score = 0;

        predictionUnlocked = false;


        scoreElement.textContent =
            score;

        playerScoreElement.textContent =
            score;


        unlockCard.style.display =
            "none";


        messageElement.innerHTML =
            "Reach <strong>2 points</strong> to unlock the prediction.";


        food =
            createFood();


        clearInterval(
            interval
        );


        interval =
            setInterval(
                gameLoop,
                100
            );


        canvas.focus();

    }}


    // =====================================================
    // DRAW
    // =====================================================

    function draw() {{

        ctx.clearRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        ctx.fillStyle =
            "#171717";

        ctx.fillRect(
            0,
            0,
            canvas.width,
            canvas.height
        );


        // Subtle grid

        ctx.strokeStyle =
            "#202020";

        ctx.lineWidth =
            1;


        for (
            let x = 0;
            x < canvas.width;
            x += grid
        ) {{

            ctx.beginPath();

            ctx.moveTo(
                x,
                0
            );

            ctx.lineTo(
                x,
                canvas.height
            );

            ctx.stroke();

        }}


        for (
            let y = 0;
            y < canvas.height;
            y += grid
        ) {{

            ctx.beginPath();

            ctx.moveTo(
                0,
                y
            );

            ctx.lineTo(
                canvas.width,
                y
            );

            ctx.stroke();

        }}


        // Food

        ctx.fillStyle =
            "#D8FF45";

        ctx.beginPath();

        ctx.arc(

            food.x * grid
            + grid / 2,

            food.y * grid
            + grid / 2,

            grid * 0.35,

            0,

            Math.PI * 2

        );

        ctx.fill();


        // Snake

        snake.forEach(
            (segment, index) => {{

                ctx.fillStyle =
                    index === 0
                    ? "#D8FF45"
                    : "#FFFFFF";


                ctx.beginPath();

                ctx.roundRect(

                    segment.x * grid + 2,

                    segment.y * grid + 2,

                    grid - 4,

                    grid - 4,

                    5

                );

                ctx.fill();

            }}
        );

    }}


    // =====================================================
    // SELF COLLISION ONLY
    // =====================================================

    function hitsSnake(
        head
    ) {{

        for (
            let i = 1;
            i < snake.length;
            i++
        ) {{

            if (
                head.x === snake[i].x &&
                head.y === snake[i].y
            ) {{

                return true;

            }}

        }}


        return false;

    }}


    // =====================================================
    // AUTO PREDICTION
    // =====================================================

    async function unlockPrediction() {{

        if (
            predictionUnlocked
        ) {{
            return;
        }}


        predictionUnlocked =
            true;


        messageElement.innerHTML =
            "<strong>Unlocked.</strong> Calculating your fare...";


        predictionElement.textContent =
            "...";


        unlockCard.style.display =
            "block";


        const query =
            new URLSearchParams(
                API_PARAMS
            );


        try {{

            const response =
                await fetch(
                    API_URL
                    + "?"
                    + query.toString()
                );


            if (
                !response.ok
            ) {{

                throw new Error(
                    "API error"
                );

            }}


            const data =
                await response.json();


            const fare =
                Number(
                    data.fare
                );


            predictionElement.textContent =
                "$"
                + fare.toFixed(2);


            messageElement.innerHTML =
                "<strong>Prediction unlocked.</strong> Keep playing to improve your score.";


        }}

        catch (error) {{

            predictionElement.textContent =
                "Unavailable";


            messageElement.textContent =
                "Unable to retrieve the prediction.";

        }}

    }}


    // =====================================================
    // GAME LOOP
    // =====================================================

    function gameLoop() {{

        dx =
            nextDx;

        dy =
            nextDy;


        let newX =
            snake[0].x + dx;

        let newY =
            snake[0].y + dy;


        // ---------------------------------------------
        // WRAP AROUND BORDERS
        // ---------------------------------------------

        if (
            newX < 0
        ) {{

            newX =
                cols - 1;

        }}


        if (
            newX >= cols
        ) {{

            newX =
                0;

        }}


        if (
            newY < 0
        ) {{

            newY =
                rows - 1;

        }}


        if (
            newY >= rows
        ) {{

            newY =
                0;

        }}


        const head = {{

            x:
                newX,

            y:
                newY

        }};


        // ---------------------------------------------
        // SELF COLLISION
        // ---------------------------------------------

        if (
            hitsSnake(head)
        ) {{

            clearInterval(
                interval
            );


            messageElement.innerHTML =
                "<strong>Game over.</strong> Press restart to try again.";


            updateLeaderboard();

            return;

        }}


        snake.unshift(
            head
        );


        // ---------------------------------------------
        // FOOD
        // ---------------------------------------------

        if (
            head.x === food.x &&
            head.y === food.y
        ) {{

            score += 1;


            scoreElement.textContent =
                score;

            playerScoreElement.textContent =
                score;


            food =
                createFood();


            updateLeaderboard();


            // -----------------------------------------
            // AUTO UNLOCK AFTER 2 POINTS
            // -----------------------------------------

            if (
                score >= TARGET_SCORE &&
                !predictionUnlocked
            ) {{

                unlockPrediction();

            }}


        }}

        else {{

            snake.pop();

        }}


        draw();

    }}


    // =====================================================
    // LEADERBOARD
    // =====================================================

    function updateLeaderboard() {{

        const players = [

            {{
                name:
                    "Snake King",

                score:
                    12
            }},

            {{
                name:
                    "Taxi Racer",

                score:
                    8
            }},

            {{
                name:
                    "NYC Driver",

                score:
                    5
            }},

            {{
                name:
                    "You",

                score:
                    score
            }}

        ];


        players.sort(
            (a, b) =>
                b.score - a.score
        );


        const table =
            document.getElementById(
                "leaderboard"
            );


        table.innerHTML =
            "";


        players.forEach(
            (player, index) => {{

                const row =
                    document.createElement(
                        "tr"
                    );


                row.innerHTML = `

                    <td class="rank">
                        ${{index + 1}}
                    </td>

                    <td>
                        ${{player.name}}
                    </td>

                    <td
                        class="leader-score"
                        ${{player.name === "You"
                            ? 'id="player-score"'
                            : ''
                        }}
                    >

                        ${{player.score}}

                    </td>

                `;


                table.appendChild(
                    row
                );

            }}
        );

    }}


    // =====================================================
    // CONTROLS
    // =====================================================

    function changeDirection(
        event
    ) {{

        const key =
            event.key;


        if (
            [
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight"
            ].includes(key)
        ) {{

            event.preventDefault();

        }}


        if (
            key === "ArrowUp" &&
            dy !== 1
        ) {{

            nextDx = 0;
            nextDy = -1;

        }}


        if (
            key === "ArrowDown" &&
            dy !== -1
        ) {{

            nextDx = 0;
            nextDy = 1;

        }}


        if (
            key === "ArrowLeft" &&
            dx !== 1
        ) {{

            nextDx = -1;
            nextDy = 0;

        }}


        if (
            key === "ArrowRight" &&
            dx !== -1
        ) {{

            nextDx = 1;
            nextDy = 0;

        }}

    }}


    canvas.addEventListener(
        "keydown",
        changeDirection
    );


    window.addEventListener(
        "keydown",
        changeDirection
    );


    restartButton.addEventListener(
        "click",
        resetGame
    );


    // =====================================================
    // START
    // =====================================================

    resetGame();

    draw();

</script>
"""


components.html(
    snake_html,
    height=590,
    scrolling=False
)

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
