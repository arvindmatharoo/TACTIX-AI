import os
import sys
import streamlit as st
import plotly.graph_objects as go

# ------------------------------------------------
# Project Path Setup
# ------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from source.engine.tactix_prediction_engine import TactixEngine

engine = TactixEngine(PROJECT_ROOT)

# ------------------------------------------------
# Background Function
# ------------------------------------------------

def set_background(image_file):

    image_path = os.path.join(PROJECT_ROOT, "frontend", image_file)

    with open(image_path, "rb") as file:
        encoded = file.read()

    import base64
    encoded_string = base64.b64encode(encoded).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        }}

        .result-card {{
        background-color: rgba(0,0,0,0.75);
        padding: 20px;
        border-radius: 12px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="TACTIX AI - Match Prediction",
    layout="wide"
)

set_background("bg_main.jpg")



st.markdown(
"""
<style>

h1, h2, h3, h4, h5, h6 {
    background-color: rgba(0,0,0,0.70);
    padding: 8px 12px;
    border-radius: 8px;
    display: inline-block;
}

p, label {
    background-color: rgba(0,0,0,0.60);
    padding: 6px 10px;
    border-radius: 6px;
    display: inline-block;
}

.stMarkdown {
    color: white;
}

</style>
""",
unsafe_allow_html=True
)

# ------------------------------------------------
# Header
# ------------------------------------------------

st.header("⚽ Match Prediction")
st.markdown("Predict match outcome and expected goals using TACTIX AI")

# ------------------------------------------------
# Metric Descriptions
# ------------------------------------------------

st.subheader("Metric Descriptions")

st.markdown("""
**Home Form / Away Form (-5 to 5)**  
Recent performance trend.

**Attack Strength (0 to 5)**  
Offensive capability.

**Defense Strength (0 to 5)**  
Defensive solidity.
""")

# ------------------------------------------------
# Slider Input Function
# ------------------------------------------------

def slider_input(label, minv, maxv, default):

    col1, col2 = st.columns([3,1])

    with col1:
        val = st.slider(label, minv, maxv, default)

    with col2:
        val = st.number_input(
            f"{label} (exact)",
            min_value=minv,
            max_value=maxv,
            value=float(val)
        )

    return val

# ------------------------------------------------
# Input Metrics
# ------------------------------------------------

st.subheader("Enter Match Metrics")

home_form = slider_input("Home Form",-5.0,5.0,0.0)
away_form = slider_input("Away Form",-5.0,5.0,0.0)

home_attack = slider_input("Home Attack",0.0,5.0,1.0)
away_attack = slider_input("Away Attack",0.0,5.0,1.0)

home_defense = slider_input("Home Defense",0.0,5.0,1.0)
away_defense = slider_input("Away Defense",0.0,5.0,1.0)

# ------------------------------------------------
# Automatically Compute Derived Features
# ------------------------------------------------

form_difference = home_form - away_form
attack_vs_defense = home_attack - away_defense
goal_difference = home_attack - away_attack

# ------------------------------------------------
# Prediction
# ------------------------------------------------

if st.button("Predict Match"):

    features = [
        home_form,
        away_form,
        home_attack,
        away_attack,
        home_defense,
        away_defense,
        form_difference,
        attack_vs_defense,
        goal_difference
    ]

    prediction = engine.predict(features)

    outcome = prediction["match_outcome_probabilities"]
    home_xg = prediction["home_expected_goals"]
    away_xg = prediction["away_expected_goals"]
    playstyle = prediction["playstyle_cluster"]

    st.subheader("Prediction Result")

    # ------------------------------------------------
    # Metric Cards
    # ------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric("Match Outcome", outcome)
    c2.metric("Home xG", round(home_xg,2))
    c3.metric("Away xG", round(away_xg,2))

    st.success(f"Tactical Style Identified: {playstyle}")

    # ------------------------------------------------
    # xG Comparison Chart
    # ------------------------------------------------

    st.subheader("Expected Goals Comparison")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Home Team"],
        y=[home_xg],
        name="Home xG"
    ))

    fig.add_trace(go.Bar(
        x=["Away Team"],
        y=[away_xg],
        name="Away xG"
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------
    # Win Probability Visualization
    # ------------------------------------------------

    st.subheader("Win Probability Estimate")

    if outcome == "Home Win":
        probs = [0.65,0.20,0.15]

    elif outcome == "Away Win":
        probs = [0.15,0.20,0.65]

    else:
        probs = [0.30,0.40,0.30]

    prob_fig = go.Figure(data=[go.Bar(
        x=["Home Win","Draw","Away Win"],
        y=probs
    )])

    st.plotly_chart(prob_fig, use_container_width=True)

    # ------------------------------------------------
    # Prediction Confidence
    # ------------------------------------------------

    confidence = max(probs)

    if confidence > 0.65:
        level = "High Confidence"
    elif confidence > 0.50:
        level = "Medium Confidence"
    else:
        level = "Low Confidence"

    st.info(f"Prediction Confidence Level: **{level}**")