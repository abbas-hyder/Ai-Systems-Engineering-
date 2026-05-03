import os
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


HISTORY_FILE = "student_history.csv"


LEVEL_MAP = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3
}


def save_attempt(topic, level, score, total):
    accuracy = score / total if total > 0 else 0

    new_row = pd.DataFrame([{
        "topic": topic,
        "level": level,
        "level_encoded": LEVEL_MAP.get(level, 1),
        "score": score,
        "total": total,
        "accuracy": accuracy
    }])

    if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
        try:
            df = pd.read_csv(HISTORY_FILE)
            df = pd.concat([df, new_row], ignore_index=True)
        except pd.errors.EmptyDataError:
            df = new_row
    else:
        df = new_row

    df["attempt_number"] = range(1, len(df) + 1)
    df["avg_accuracy_so_far"] = df["accuracy"].expanding().mean()

    df.to_csv(HISTORY_FILE, index=False)


def load_history():
    if os.path.exists(HISTORY_FILE) and os.path.getsize(HISTORY_FILE) > 0:
        try:
            return pd.read_csv(HISTORY_FILE)
        except pd.errors.EmptyDataError:
            return pd.DataFrame()

    return pd.DataFrame()

def train_accuracy_models():
    df = load_history()

    if len(df) < 5:
        return None, None, "Not enough data. Complete at least 5 quizzes."

    features = [
        "level_encoded",
        "score",
        "total",
        "attempt_number",
        "avg_accuracy_so_far"
    ]

    X = df[features]
    y = df["accuracy"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
    }

    results = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        results[name] = {
            "model": model,
            "mae": mean_absolute_error(y_test, predictions),
            "r2": r2_score(y_test, predictions)
        }

    best_model_name = min(results, key=lambda x: results[x]["mae"])
    best_model = results[best_model_name]["model"]

    return best_model, results, best_model_name


def predict_next_accuracy(level, latest_score, total):
    df = load_history()

    if len(df) < 5:
        return None

    model, results, best_model_name = train_accuracy_models()

    if model is None:
        return None

    next_attempt = len(df) + 1
    avg_accuracy = df["accuracy"].mean()

    input_data = pd.DataFrame([{
        "level_encoded": LEVEL_MAP.get(level, 1),
        "score": latest_score,
        "total": total,
        "attempt_number": next_attempt,
        "avg_accuracy_so_far": avg_accuracy
    }])

    prediction = model.predict(input_data)[0]
    prediction = np.clip(prediction, 0, 1)

    return prediction, best_model_name, results