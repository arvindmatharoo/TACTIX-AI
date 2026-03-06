import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
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
    page_title="TACTIX AI - Model Insights",
    layout="wide"
)

set_background("bg_model_insights.jpg")






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

st.header("🧠 Model Insights")
st.markdown("Understanding how the TACTIX AI models analyze football matches")

# ------------------------------------------------
# Model Overview
# ------------------------------------------------

st.subheader("Model Architecture")

st.markdown("""
TACTIX AI uses a hybrid machine learning architecture:

• Logistic Regression  
• Random Forest  
• XGBoost  
• Neural Networks (TensorFlow/Keras)

These models analyze engineered tactical features derived from match statistics to predict:

• Match Outcome  
• Expected Goals (xG)  
• Tactical Playstyle Cluster
""")

# ------------------------------------------------
# Feature Importance (Conceptual)
# ------------------------------------------------

st.subheader("Key Tactical Features")

features = [
"Home Form",
"Away Form",
"Home Attack",
"Away Attack",
"Home Defense",
"Away Defense",
"Form Difference",
"Attack vs Defense",
"Goal Difference"
]

importance = [0.11,0.10,0.18,0.17,0.15,0.14,0.05,0.05,0.05]

fig = go.Figure()

fig.add_trace(go.Bar(
    x=features,
    y=importance
))

fig.update_layout(
    title="Conceptual Feature Importance"
)

st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Feature Distribution
# ------------------------------------------------

st.subheader("Feature Distribution")

feature_choice = st.selectbox(
"Select Feature",
[
"home_attack",
"away_attack",
"home_defense",
"away_defense",
"home_form",
"away_form"
]
)

fig2 = px.histogram(
    dataset[feature_choice],
    nbins=30
)

st.plotly_chart(fig2,use_container_width=True)

# ------------------------------------------------
# Feature Relationships
# ------------------------------------------------

st.subheader("Feature Relationship Explorer")

x_feature = st.selectbox(
"X Axis Feature",
[
"home_attack",
"away_attack",
"home_defense",
"away_defense",
"home_form",
"away_form"
],
key="x_feature"
)

y_feature = st.selectbox(
"Y Axis Feature",
[
"home_attack",
"away_attack",
"home_defense",
"away_defense",
"home_form",
"away_form"
],
key="y_feature"
)

fig3 = px.scatter(
dataset,
x=x_feature,
y=y_feature
)

st.plotly_chart(fig3,use_container_width=True)

# ------------------------------------------------
# Prediction Feature Summary
# ------------------------------------------------

st.subheader("Prediction Feature Summary")

summary = pd.DataFrame({
"Feature":[
"Home Attack",
"Away Attack",
"Home Defense",
"Away Defense",
"Home Form",
"Away Form"
],
"Mean":[
dataset["home_attack"].mean(),
dataset["away_attack"].mean(),
dataset["home_defense"].mean(),
dataset["away_defense"].mean(),
dataset["home_form"].mean(),
dataset["away_form"].mean()
]
})

st.dataframe(summary)