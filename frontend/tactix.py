import os
import streamlit as st
import base64

# ------------------------------------------------
# Page Configuration
# ------------------------------------------------

st.set_page_config(
    page_title="TACTIX AI",
    page_icon="⚽",
    layout="wide"
)

# ------------------------------------------------
# Background Function
# ------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

def set_background(image_file):

    image_path = os.path.join(PROJECT_ROOT, image_file)

    with open(image_path, "rb") as file:
        encoded = file.read()

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

        .title-box {{
            background-color: rgba(0,0,0,0.75);
            padding: 30px;
            border-radius: 12px;
            text-align:center;
        }}

        .text-box {{
            background-color: rgba(0,0,0,0.65);
            padding: 20px;
            border-radius: 10px;
            margin-top:10px;
        }}

        .page-card {{
            background-color: rgba(0,0,0,0.60);
            padding: 18px;
            border-radius: 10px;
            margin-bottom:10px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# Apply Background
# ------------------------------------------------

set_background("tactix.jpg")

# ------------------------------------------------
# Title Section
# ------------------------------------------------

st.markdown(
"""
<div class="title-box">

<h1>⚽ TACTIX AI</h1>
<h3>Football Tactical Intelligence System</h3>

</div>
""",
unsafe_allow_html=True
)

st.write("")

# ------------------------------------------------
# Description Section
# ------------------------------------------------

st.markdown(
"""
<div class="text-box">

TACTIX AI is an advanced football analytics platform designed to analyze tactical match dynamics using machine learning and statistical modeling. Built on top of the European Soccer Database, the system processes match statistics and engineered tactical features to generate intelligent predictions and insights about football matches. The platform combines multiple machine learning approaches including Logistic Regression, Random Forest, XGBoost, and Neural Networks to understand patterns in team performance, attacking efficiency, defensive strength, and form dynamics.

The objective of TACTIX AI is to transform raw football data into actionable tactical intelligence. By analyzing metrics such as team form, attacking capabilities, defensive solidity, and expected goals (xG), the system predicts match outcomes and identifies tactical patterns that influence performance. The platform also provides analytical dashboards for exploring historical matches, comparing team performance, studying dataset statistics, and running large-scale predictions. TACTIX AI demonstrates how machine learning and data science can be applied to football analytics to uncover meaningful insights about the game.

</div>
""",
unsafe_allow_html=True
)

st.write("")
st.write("")

# ------------------------------------------------
# Platform Features
# ------------------------------------------------

st.markdown("## Platform Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
    """
    <div class="page-card">
    <h4>⚽ Match Prediction</h4>
    Predict match outcomes and expected goals using tactical features such as team form, attacking strength, and defensive performance.
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="page-card">
    <h4>⚙️ Tactical Analysis</h4>
    Visualize and compare tactical metrics between teams using radar charts and performance comparisons.
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="page-card">
    <h4>📊 Team Comparison</h4>
    Compare teams based on goals, attack strength, defense capability, and recent form trends.
    </div>
    """,
    unsafe_allow_html=True
    )

with col2:

    st.markdown(
    """
    <div class="page-card">
    <h4>🔍 Match Explorer</h4>
    Explore historical matches between teams and analyze detailed match statistics and tactical metrics.
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="page-card">
    <h4>📈 Dataset Analytics</h4>
    Investigate statistical patterns in the dataset including goal distributions, form trends, and feature relationships.
    </div>
    """,
    unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="page-card">
    <h4>🧠 Model Insights</h4>
    Understand how the machine learning models analyze tactical features and how different metrics influence predictions.
    </div>
    """,
    unsafe_allow_html=True
    )

st.markdown(
"""
<div class="page-card">
<h4>📂 Batch Predictions</h4>
Upload large datasets of matches and generate predictions for multiple games simultaneously.
</div>
""",
unsafe_allow_html=True
)

st.write("")
st.write("")

# ------------------------------------------------
# Navigation Hint
# ------------------------------------------------

st.info("Use the sidebar to navigate through the TACTIX AI platform modules.")