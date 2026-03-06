import numpy as np
import os
import joblib
import pandas as pd

class TactixEngine:
    def __init__(self, project_root):

        model_path = os.path.join(project_root, "models")

        #load match predictor
        self.match_model = joblib.load(os.path.join(model_path, "tactix_match_predictor.pkl"))

        self.match_scaler = joblib.load(os.path.join(model_path, "tactix_scaler.pkl"))

        #load xG models

        self.home_xg_model = joblib.load(os.path.join(model_path, "home_xg_model.pkl"))

        self.away_xg_model = joblib.load(os.path.join(model_path, "away_xg_model.pkl"))

        self.xg_scaler =   joblib.load(os.path.join(model_path, "xg_scaler.pkl"))

        #LOAD playstyle model

        self.playstyle_model = joblib.load(os.path.join(model_path, "playstyle_cluster_model.pkl"))

        self.playstyle_scaler = joblib.load(os.path.join(model_path, "playstyle_scaler.pkl"))




    def predict(self, features):

        columns = [
            "home_form",
            "away_form",
            "home_attack",
            "away_attack",
            "home_defense",
            "away_defense",
            "form_difference",
            "attack_vs_defense",
            "goal_difference"
        ]

        features = pd.DataFrame([features], columns=columns)

        # ------------------------------------------------
        # MATCH PREDICTION MODEL
        # ------------------------------------------------

        match_features = features.iloc[:, :8]

        scaled_match = self.match_scaler.transform(match_features)

        outcome_class = self.match_model.predict(scaled_match)[0]

        outcome_map = {
            0: "Home Win",
            1: "Draw",
            2: "Away Win"
        }

        outcome = outcome_map[int(outcome_class)]

        # ------------------------------------------------
        # EXPECTED GOALS MODEL
        # ------------------------------------------------

        xg_scaled = self.xg_scaler.transform(match_features)

        home_xg = self.home_xg_model.predict(xg_scaled)[0]
        away_xg = self.away_xg_model.predict(xg_scaled)[0]

        # ------------------------------------------------
        # CREATE PLAYSTYLE FEATURES
        # ------------------------------------------------

        playstyle_features = pd.DataFrame()

        playstyle_features["home_attack"] = features["home_attack"]
        playstyle_features["away_attack"] = features["away_attack"]
        playstyle_features["home_defense"] = features["home_defense"]
        playstyle_features["away_defense"] = features["away_defense"]

        playstyle_features["attack_balance"] = (
            features["home_attack"] - features["away_attack"]
        )

        playstyle_features["defense_balance"] = (
            features["home_defense"] - features["away_defense"]
        )

        playstyle_features["form_balance"] = (
            features["home_form"] - features["away_form"]
        )

        playstyle_features["goal_potential"] = (
            features["home_attack"] + features["away_attack"]
        )

        playstyle_features["goal_difference"] = features["goal_difference"]

        # ------------------------------------------------
        # PLAYSTYLE MODEL
        # ------------------------------------------------

        playstyle_scaled = self.playstyle_scaler.transform(playstyle_features)

        cluster = self.playstyle_model.predict(playstyle_scaled)[0]

        playstyle_map = {
            0: "Possession",
            1: "Counter Attack",
            2: "Defensive",
            3: "Wide Play",
            4: "Long Ball"
        }

        playstyle = playstyle_map.get(int(cluster), "Unknown")

        return {
            "match_outcome_probabilities": outcome,
            "home_expected_goals": float(home_xg),
            "away_expected_goals": float(away_xg),
            "playstyle_cluster": playstyle
        }