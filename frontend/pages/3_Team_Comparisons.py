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
    page_title="TACTIX AI - Team Comparison",
    layout="wide"
)

set_background("bg_last.jpg")


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

st.header("📊 Team Comparison")
st.markdown("Compare tactical and statistical performance between two teams")

# ------------------------------------------------
# Team Selection
# ------------------------------------------------

teams = sorted(dataset["home_team_name"].unique())

col1,col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Select Team 1",teams)

with col2:
    team2 = st.selectbox("Select Team 2",teams)

# ------------------------------------------------
# Filter Data
# ------------------------------------------------

team1_data = dataset[dataset["home_team_name"] == team1]
team2_data = dataset[dataset["home_team_name"] == team2]

# ------------------------------------------------
# Compute Statistics
# ------------------------------------------------

stats = pd.DataFrame({
    "Metric":["Goals","Attack","Defense","Form"],
    team1:[
        team1_data["home_team_goal"].mean(),
        team1_data["home_attack"].mean(),
        team1_data["home_defense"].mean(),
        team1_data["home_form"].mean()
    ],
    team2:[
        team2_data["home_team_goal"].mean(),
        team2_data["home_attack"].mean(),
        team2_data["home_defense"].mean(),
        team2_data["home_form"].mean()
    ]
})

# ------------------------------------------------
# Show Table
# ------------------------------------------------

st.subheader("Statistical Comparison")

st.dataframe(stats)

# ------------------------------------------------
# Bar Chart Comparison
# ------------------------------------------------

fig = go.Figure()

fig.add_trace(go.Bar(
    x=stats["Metric"],
    y=stats[team1],
    name=team1
))

fig.add_trace(go.Bar(
    x=stats["Metric"],
    y=stats[team2],
    name=team2
))

fig.update_layout(
    title="Team Performance Comparison",
    barmode="group"
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Tactical Radar Chart
# ------------------------------------------------

st.subheader("Tactical Radar Comparison")

categories = ["Attack","Defense","Form"]

team1_values = [
    team1_data["home_attack"].mean(),
    team1_data["home_defense"].mean(),
    team1_data["home_form"].mean()
]

team2_values = [
    team2_data["home_attack"].mean(),
    team2_data["home_defense"].mean(),
    team2_data["home_form"].mean()
]

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
    r=team1_values,
    theta=categories,
    fill='toself',
    name=team1
))

radar.add_trace(go.Scatterpolar(
    r=team2_values,
    theta=categories,
    fill='toself',
    name=team2
))

radar.update_layout(
    polar=dict(
        radialaxis=dict(visible=True)
    ),
    showlegend=True
)

st.plotly_chart(radar,use_container_width=True)

# ------------------------------------------------
# Tactical Advantage Indicator
# ------------------------------------------------

st.subheader("Tactical Advantage")

team1_score = sum(team1_values)
team2_score = sum(team2_values)

if team1_score > team2_score:
    st.success(f"{team1} shows stronger tactical performance")

elif team2_score > team1_score:
    st.success(f"{team2} shows stronger tactical performance")

else:
    st.info("Both teams appear tactically balanced")