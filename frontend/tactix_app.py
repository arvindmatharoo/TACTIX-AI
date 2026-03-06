import os
import sys
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

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


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from source.engine.tactix_prediction_engine import TactixEngine

engine = TactixEngine(PROJECT_ROOT)

data_path = os.path.join(PROJECT_ROOT,"data/processed/match_features.csv")
dataset = pd.read_csv(data_path)

st.set_page_config(page_title="TACTIX AI",layout="wide")



# ------------------------------------------------
# Header
# ------------------------------------------------

st.markdown("# ⚽ TACTIX AI Football Intelligence Platform")
st.markdown("### Match Prediction • Tactical Analysis • Data Explorer")



# ------------------------------------------------
# Sidebar
# ------------------------------------------------

menu = st.sidebar.radio(
"Navigation",
[
"Manual Prediction",
"Batch Prediction",
"Match Explorer",
"Dataset Analytics",
"Team Comparison"
]
)
#------------------------------------------------
#Adding Background IMages 
#------------------------------------------------
if menu == "Manual Prediction":
    set_background("bg_main.jpg")

elif menu == "Batch Prediction":
    set_background("batch_bg.jpg")

elif menu == "Match Explorer":
    set_background("bg_comparison.jpg")

elif menu == "Dataset Analytics":
    set_background("bg_analysis.jpg")

elif menu == "Team Comparison":
    set_background("bg_last.jpg")

#------------------------------------------------
#Adding text styling 
#------------------------------------------------
def style_text():

    st.markdown(
        """
        <style>

        h1, h2, h3, h4, h5, h6 {
            background-color: rgba(0,0,0,0.65);
            padding: 8px;
            border-radius: 6px;
            display: inline-block;
        }

        p, label {
            background-color: rgba(0,0,0,0.55);
            padding: 6px;
            border-radius: 5px;
            display: inline-block;
        }

        .stMarkdown {
            color: white;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

style_text()

# ------------------------------------------------
# Manual Prediction
# ------------------------------------------------

if menu == "Manual Prediction":

    st.header("Manual Match Prediction")

    st.markdown("### Metric Descriptions")

    st.markdown("""
**Home Form / Away Form (-5 to 5)**  
Recent performance trend of the team.

**Attack Strength (0 to 5)**  
Offensive capability based on scoring patterns.

**Defense Strength (0 to 5)**  
Defensive solidity based on goals conceded.

**Form Difference (-5 to 5)**  
Difference in recent performance between teams.

**Attack vs Defense (-5 to 5)**  
Relative attacking vs defensive balance.

**Goal Difference (-5 to 5)**  
Expected goal difference indicator.
""")

    def slider_input(label,minv,maxv,default):

        col1,col2 = st.columns([3,1])

        with col1:
            val = st.slider(label,minv,maxv,default)

        with col2:
            val = st.number_input(
                f"{label} (exact)",
                min_value=minv,
                max_value=maxv,
                value=float(val)
            )

        return val

    st.subheader("Enter Match Metrics")

    home_form = slider_input("Home Form",-5.0,5.0,0.0)
    away_form = slider_input("Away Form",-5.0,5.0,0.0)

    home_attack = slider_input("Home Attack",0.0,5.0,1.0)
    away_attack = slider_input("Away Attack",0.0,5.0,1.0)

    home_defense = slider_input("Home Defense",0.0,5.0,1.0)
    away_defense = slider_input("Away Defense",0.0,5.0,1.0)

    form_difference = slider_input("Form Difference",-5.0,5.0,0.0)
    attack_vs_defense = slider_input("Attack vs Defense",-5.0,5.0,0.0)
    goal_difference = slider_input("Goal Difference",-5.0,5.0,0.0)

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

        st.subheader("Prediction Result")

        c1,c2,c3 = st.columns(3)

        c1.metric("Match Outcome",prediction["match_outcome_probabilities"])
        c2.metric("Home xG",round(prediction["home_expected_goals"],2))
        c3.metric("Away xG",round(prediction["away_expected_goals"],2))

        st.success(f"Tactical Style: {prediction['playstyle_cluster']}")

        fig = go.Figure(data=[go.Bar(
            x=["Home xG","Away xG"],
            y=[prediction["home_expected_goals"],
               prediction["away_expected_goals"]]
        )])

        st.plotly_chart(fig,use_container_width=True)

# ------------------------------------------------
# Batch Prediction 
# ------------------------------------------------

elif menu == "Batch Prediction":

    st.header("Batch Prediction")

    st.markdown("""
### Upload CSV File

The CSV file should contain the following columns:

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

    if file:

        df = pd.read_csv(file)

        st.subheader("Uploaded Dataset Preview")
        st.dataframe(df.head())

        if st.button("Run Predictions"):

            results=[]

            for _,row in df.iterrows():

                pred = engine.predict(row.tolist())

                results.append({
                    "match_outcome":pred["match_outcome_probabilities"],
                    "home_xG":pred["home_expected_goals"],
                    "away_xG":pred["away_expected_goals"],
                    "playstyle":pred["playstyle_cluster"]
                })

            result_df = pd.DataFrame(results)

            st.subheader("Prediction Results")
            st.dataframe(result_df)

            csv = result_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="Download Predictions",
                data=csv,
                file_name="tactix_predictions.csv",
                mime="text/csv"
            )

# ------------------------------------------------
# Match Explorer
# ------------------------------------------------

elif menu == "Match Explorer":

    st.header("Match Explorer")

    teams = sorted(dataset["home_team_name"].unique())

    teamA = st.selectbox("Select Team A",teams)
    teamB = st.selectbox("Select Team B",teams)

    matches = dataset[
        ((dataset["home_team_name"]==teamA) &
         (dataset["away_team_name"]==teamB)) |
        ((dataset["home_team_name"]==teamB) &
         (dataset["away_team_name"]==teamA))
    ]

    if len(matches)==0:
        st.warning("No matches between these teams.")

    else:

        match_list = matches.index.tolist()

        selected_match = st.selectbox(
            "Select Match",
            match_list
        )

        if st.button("View Match Details"):

            match = dataset.loc[selected_match]

            st.json(match.to_dict())

# ------------------------------------------------
# Dataset Analytics 
# ------------------------------------------------

elif menu == "Dataset Analytics":

    st.header("Dataset Analytics")

    st.subheader("Goal Distribution")
    st.markdown("Distribution of goals scored in matches.")

    fig = px.histogram(
        dataset[["home_team_goal","away_team_goal"]],
        nbins=20
    )

    st.plotly_chart(fig,use_container_width=True)


    st.subheader("Average Home vs Away Goals")
    st.markdown("Shows scoring advantage of home teams.")

    avg_home = dataset["home_team_goal"].mean()
    avg_away = dataset["away_team_goal"].mean()

    fig2 = go.Figure(data=[go.Bar(
        x=["Home Goals","Away Goals"],
        y=[avg_home,avg_away]
    )])

    st.plotly_chart(fig2,use_container_width=True)


    st.subheader("Form Distribution")
    st.markdown("Shows distribution of team form values.")

    fig3 = px.histogram(
        dataset["home_form"],
        nbins=30
    )

    st.plotly_chart(fig3,use_container_width=True)


    st.subheader("Attack vs Defense Analysis")
    st.markdown("Relationship between attacking strength and defensive strength.")

    fig4 = px.scatter(
        dataset,
        x="home_attack",
        y="home_defense"
    )

    st.plotly_chart(fig4,use_container_width=True)


    st.subheader("Goal Difference Distribution")
    st.markdown("Distribution of goal difference across matches.")

    fig5 = px.histogram(
        dataset["goal_difference"],
        nbins=30
    )

    st.plotly_chart(fig5,use_container_width=True)

# ------------------------------------------------
# Team Comparison
# ------------------------------------------------

elif menu == "Team Comparison":

    st.header("Team Comparison")

    teams = sorted(dataset["home_team_name"].unique())

    t1 = st.selectbox("Team 1",teams)
    t2 = st.selectbox("Team 2",teams)

    d1 = dataset[dataset["home_team_name"]==t1]
    d2 = dataset[dataset["home_team_name"]==t2]

    stats=pd.DataFrame({
        "Metric":["Goals","Attack","Defense","Form"],
        "Team1":[
            d1["home_team_goal"].mean(),
            d1["home_attack"].mean(),
            d1["home_defense"].mean(),
            d1["home_form"].mean()
        ],
        "Team2":[
            d2["home_team_goal"].mean(),
            d2["home_attack"].mean(),
            d2["home_defense"].mean(),
            d2["home_form"].mean()
        ]
    })

    st.dataframe(stats)

    fig=go.Figure()

    fig.add_trace(go.Bar(
        x=stats["Metric"],
        y=stats["Team1"],
        name=t1
    ))

    fig.add_trace(go.Bar(
        x=stats["Metric"],
        y=stats["Team2"],
        name=t2
    ))

    st.plotly_chart(fig,use_container_width=True)