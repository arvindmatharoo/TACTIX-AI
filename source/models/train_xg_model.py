#using XGBoost Regressor

from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import joblib

def train_xg_model(X_train, X_test, y_train, y_test):
    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=4
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)

    print("MSE: ", mse)

    return model


def save_models(home_model,away_model, scaler):
    joblib.dump(home_model, "C:/Users/arvin/OneDrive/Documents/MAIN DOCS/TACTIX-AI/models/home_xg_model.pkl")
    joblib.dump(away_model, "C:/Users/arvin/OneDrive/Documents/MAIN DOCS/TACTIX-AI/models/away_xg_model.pkl")
    joblib.dump(scaler, "C:/Users/arvin/OneDrive/Documents/MAIN DOCS/TACTIX-AI/models/xg_scaler.pkl")