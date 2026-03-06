import pandas as pd
import sqlite3
import os

from sympy import mathematica_code

from source.features.tactical_features import create_tactical_features
from source.features.expected_goals_features import create_expected_goals_targets


# Project Root


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../")
)

db_path = os.path.join(PROJECT_ROOT, "data/raw/database.sqlite")

print("Using database:", db_path)

conn = sqlite3.connect(db_path)


# Load Match Data


match_data = pd.read_sql('SELECT * FROM "Match"', conn)

print("Raw Matches Loaded:", match_data.shape)

# LOAD TEAM TABLE

team_data = pd.read_sql("SELECT team_api_id, team_long_name FROM Team", conn)

team_data = team_data.drop_duplicates(subset="team_api_id")

#Merge team names

match_data = match_data.merge(team_data, left_on='home_team_api_id', right_on='team_api_id', how='left')
match_data = match_data.rename(columns={'team_long_name':'home_team_name'})
match_data = match_data.drop(columns=['team_api_id'])


match_data = match_data.merge(team_data, left_on='away_team_api_id', right_on='team_api_id', how='left')
match_data = match_data.rename(columns={'team_long_name':'away_team_name'})
match_data = match_data.drop(columns=['team_api_id'])

# Basic Performance Features
match_data['home_attack'] = match_data['home_team_goal']
match_data['away_attack'] = match_data['away_team_goal']

match_data['home_defense'] = match_data['away_team_goal']
match_data['away_defense'] = match_data['home_team_goal']

match_data['home_form'] = match_data['home_team_goal'] - match_data['away_team_goal']
match_data['away_form'] = match_data['away_team_goal'] - match_data['home_team_goal']



# tactical features

match_data = create_tactical_features(match_data)


#Additional Features
match_data["form_difference"] = (
    match_data["home_form"] - match_data["away_form"]
)

match_data["attack_vs_defense"] = (
    match_data["home_attack"] - match_data["away_defense"]
)

# Expected Goals Targets


match_data = create_expected_goals_targets(match_data)


# Final Feature Selection


features = match_data[
[
"home_team_api_id",
"away_team_api_id",
"home_team_name",
"away_team_name",
"home_team_goal",
"away_team_goal",
"home_form",
"away_form",
"home_attack",
"away_attack",
"home_defense",
"away_defense",
"form_difference",
"attack_vs_defense",
"goal_difference",
"home_xG",
"away_xG"
]
]


output_path = os.path.join(
    PROJECT_ROOT,
    "data/processed/match_features.csv"
)

features.to_csv(output_path, index=False)

print("Processed Dataset Saved:", features.shape)