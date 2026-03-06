import os
import sys
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

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
    page_title="TACTIX AI - Dataset Analytics",
    layout="wide"
)

set_background("bg_dataset.jpg")





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

st.header("📈 Dataset Analytics")
st.markdown("Explore statistical patterns within the football dataset")

# ------------------------------------------------
# Goal Distribution
# ------------------------------------------------

st.subheader("Goal Distribution")

fig1 = px.histogram(
    dataset[["home_team_goal","away_team_goal"]],
    nbins=20
)

st.plotly_chart(fig1,use_container_width=True)

# ------------------------------------------------
# Average Home vs Away Goals
# ------------------------------------------------

st.subheader("Average Home vs Away Goals")

avg_home = dataset["home_team_goal"].mean()
avg_away = dataset["away_team_goal"].mean()

fig2 = go.Figure(data=[go.Bar(
    x=["Home Goals","Away Goals"],
    y=[avg_home,avg_away]
)])

st.plotly_chart(fig2,use_container_width=True)

# ------------------------------------------------
# Form Distribution
# ------------------------------------------------

st.subheader("Form Distribution")

fig3 = px.histogram(
    dataset["home_form"],
    nbins=30
)

st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# Attack vs Defense Analysis
# ------------------------------------------------

st.subheader("Attack vs Defense Relationship")

fig4 = px.scatter(
    dataset,
    x="home_attack",
    y="home_defense"
)

st.plotly_chart(fig4,use_container_width=True)

# ------------------------------------------------
# Goal Difference Distribution
# ------------------------------------------------

st.subheader("Goal Difference Distribution")

fig5 = px.histogram(
    dataset["goal_difference"],
    nbins=30
)

st.plotly_chart(fig5,use_container_width=True)

# ------------------------------------------------
# Dataset Summary
# ------------------------------------------------

st.subheader("Dataset Overview")

col1,col2,col3 = st.columns(3)

col1.metric("Total Matches",len(dataset))
col2.metric("Unique Teams",dataset["home_team_name"].nunique())
col3.metric("Average Goals Per Match",
            round(dataset["home_team_goal"].mean()+dataset["away_team_goal"].mean(),2))