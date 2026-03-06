import os
import sys
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
    page_title="TACTIX AI - Tactical Analysis",
    layout="wide"
)

set_background("bg_analysis.jpg")

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
# Header
# ------------------------------------------------

st.header("⚙️ Tactical Analysis")
st.markdown("Visualize tactical strengths and weaknesses of both teams")

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

st.subheader("Team Tactical Metrics")

home_attack = slider_input("Home Attack",0.0,5.0,1.0)
away_attack = slider_input("Away Attack",0.0,5.0,1.0)

home_defense = slider_input("Home Defense",0.0,5.0,1.0)
away_defense = slider_input("Away Defense",0.0,5.0,1.0)

home_form = slider_input("Home Form",-5.0,5.0,0.0)
away_form = slider_input("Away Form",-5.0,5.0,0.0)

# ------------------------------------------------
# Radar Chart
# ------------------------------------------------

st.subheader("Tactical Radar Comparison")

categories = ["Attack","Defense","Form"]

home_values = [home_attack, home_defense, home_form]
away_values = [away_attack, away_defense, away_form]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=home_values,
    theta=categories,
    fill='toself',
    name='Home Team'
))

fig.add_trace(go.Scatterpolar(
    r=away_values,
    theta=categories,
    fill='toself',
    name='Away Team'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True)
    ),
    showlegend=True
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Attack Comparison
# ------------------------------------------------

st.subheader("Attack Strength Comparison")

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    x=["Home","Away"],
    y=[home_attack,away_attack],
    name="Attack"
))

st.plotly_chart(fig2,use_container_width=True)

# ------------------------------------------------
# Defense Comparison
# ------------------------------------------------

st.subheader("Defense Strength Comparison")

fig3 = go.Figure()

fig3.add_trace(go.Bar(
    x=["Home","Away"],
    y=[home_defense,away_defense],
    name="Defense"
))

st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# Form Comparison
# ------------------------------------------------

st.subheader("Form Comparison")

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=["Home","Away"],
    y=[home_form,away_form],
    name="Form"
))

st.plotly_chart(fig4,use_container_width=True)

# ------------------------------------------------
# Tactical Advantage Indicator
# ------------------------------------------------

st.subheader("Tactical Advantage")

home_score = home_attack + home_defense + home_form
away_score = away_attack + away_defense + away_form

if home_score > away_score:
    st.success("Home Team has Tactical Advantage")

elif away_score > home_score:
    st.success("Away Team has Tactical Advantage")

else:
    st.info("Teams appear tactically balanced")