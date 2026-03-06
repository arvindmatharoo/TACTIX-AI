import os
import sys
import pandas as pd
import streamlit as st

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
        </style>
        """,
        unsafe_allow_html=True
    )

# ------------------------------------------------
# Page Config
# ------------------------------------------------

st.set_page_config(
    page_title="TACTIX AI - Batch Predictions",
    layout="wide"
)

set_background("batch_bg.jpg")






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

st.header("📂 Batch Match Predictions")
st.markdown("Upload a dataset of matches and generate predictions using TACTIX AI")

# ------------------------------------------------
# Upload File
# ------------------------------------------------

st.subheader("Upload CSV File")

st.markdown("""
Your CSV must contain the following columns:

home_form  
away_form  
home_attack  
away_attack  
home_defense  
away_defense  
form_difference  
attack_vs_defense  
goal_difference
""")

file = st.file_uploader("Upload Prediction Dataset (CSV)")

# ------------------------------------------------
# Process File
# ------------------------------------------------

if file:

    df = pd.read_csv(file)

    st.subheader("Uploaded Dataset Preview")
    st.dataframe(df.head())

    if st.button("Run Batch Predictions"):

        results = []

        for _, row in df.iterrows():

            pred = engine.predict(row.tolist())

            results.append({
                "match_outcome": pred["match_outcome_probabilities"],
                "home_xG": pred["home_expected_goals"],
                "away_xG": pred["away_expected_goals"],
                "playstyle_cluster": pred["playstyle_cluster"]
            })

        result_df = pd.DataFrame(results)

        st.subheader("Prediction Results")

        st.dataframe(result_df)

        # ------------------------------------------------
        # Download Predictions
        # ------------------------------------------------

        csv = result_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Predictions",
            data=csv,
            file_name="tactix_batch_predictions.csv",
            mime="text/csv"
        )