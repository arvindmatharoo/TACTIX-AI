#to train a K-Means Clustering Model telling about the type of play the team shows
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def train_playstyle_model(tactical_data):

    features = [
    "home_attack",
        "away_attack",
        "home_defense",
        "away_defense",
        "attack_balance",
        "defense_balance",
        "form_balance",
        "goal_potential",
        "goal_difference"
    ]
    X = tactical_data[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters = 5,
        random_state=42
    )

    clusters = model.fit_predict(X_scaled)

    tactical_data["playstyle_clsuter"] = clusters

    return model, scaler, tactical_data

