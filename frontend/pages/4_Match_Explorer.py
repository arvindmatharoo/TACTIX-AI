import os
import sys
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ------------------------------------------------
# Project Path Setup
# ------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

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
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="TACTIX AI - Match Explorer",
    layout="wide"
)

set_background("bg_comparison.jpg")




st.markdown(
"""
<style>

h1, h2, h3, h4, h5, h6 {
    background-color: rgba(0,0,0,0.70);
    padding: 8px 12px;
    border-radius: 8px;
    display: block;
    text-align: center;
}

p, label {
    background-color: rgba(0,0,0,0.60);
    padding: 6px 10px;
    border-radius: 6px;
    display: block;
    text-align: center;
}

.stMarkdown {
    color: white;
}

</style>
""",
unsafe_allow_html=True
)

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

data_path = os.path.join(PROJECT_ROOT,"data/processed/match_features.csv")
dataset = pd.read_csv(data_path)

# ------------------------------------------------
# Header
# ------------------------------------------------

st.header("🔍 Match Explorer")
st.markdown("Explore historical matches and analyze team performance")

# ------------------------------------------------
# Team Selection
# ------------------------------------------------

teams = sorted(dataset["home_team_name"].unique())

col1, col2 = st.columns(2)

with col1:
    teamA = st.selectbox("Select Team A", teams)

with col2:
    teamB = st.selectbox("Select Team B", teams)

# ------------------------------------------------
# Filter Matches
# ------------------------------------------------

matches = dataset[
    ((dataset["home_team_name"] == teamA) & (dataset["away_team_name"] == teamB)) |
    ((dataset["home_team_name"] == teamB) & (dataset["away_team_name"] == teamA))
]

# ------------------------------------------------
# Show Matches
# ------------------------------------------------

if len(matches) == 0:

    st.warning("No matches found between these teams.")

else:

    st.subheader("Matches Between Teams")

    match_list = matches.index.tolist()

    selected_match = st.selectbox(
        "Select Match",
        match_list
    )

    if st.button("View Match Analysis"):

        match = dataset.loc[selected_match]

        # ------------------------------------------------
        # Show Match Details
        # ------------------------------------------------

        st.subheader("Match Details")

        c1, c2, c3 = st.columns(3)

        c1.metric("Home Team", match["home_team_name"])
        c2.metric("Home Goals", match["home_team_goal"])
        c3.metric("Away Goals", match["away_team_goal"])

        st.write("")

        # ------------------------------------------------
        # Tactical Metrics
        # ------------------------------------------------

        st.subheader("Tactical Metrics")

        metrics = [
            "home_attack",
            "away_attack",
            "home_defense",
            "away_defense",
            "home_form",
            "away_form"
        ]

        metric_values = [
            match["home_attack"],
            match["away_attack"],
            match["home_defense"],
            match["away_defense"],
            match["home_form"],
            match["away_form"]
        ]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=metrics,
            y=metric_values
        ))

        st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------------
        # Goal Comparison
        # ------------------------------------------------

        st.subheader("Goal Comparison")

        fig2 = go.Figure()

        fig2.add_trace(go.Bar(
            x=["Home Goals","Away Goals"],
            y=[match["home_team_goal"],match["away_team_goal"]]
        ))

        st.plotly_chart(fig2,use_container_width=True)

        # ------------------------------------------------
        # Match Data
        # ------------------------------------------------

        st.subheader("Full Match Data")

        st.json(match.to_dict())