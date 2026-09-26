"""
MINEGUARD - Model Training Script
Team VORTEX# | SIH 2026 | PS 26025

Trains Random Forest (supervised) and Isolation Forest (unsupervised)
on the literature-threshold labelled dataset.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE, "data", "mineguard_sensor_dataset.csv")
MODEL_DIR = os.path.join(BASE, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

FEATURE_COLS = [
    "tilt", "vibration", "moisture", "strain", "crack_gap", "rssi", "acoustic",
    "tilt_vibration_product", "strain_crack_ratio", "signal_anomaly",
]

def main():
    print("Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    print(f"Samples: {len(df)} | Risk samples: {df['label'].sum()}")

    X = df[FEATURE_COLS]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    # ---- Random Forest ----
    print("\nTraining Random Forest...")
    rf = RandomForestClassifier(
        n_estimators=100, max_depth=8, random_state=42, class_weight="balanced"
    )
    rf.fit(X_train_s, y_train)
    y_pred = rf.predict(X_test_s)
    print(classification_report(y_test, y_pred, target_names=["Normal", "Subsidence Risk"]))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    importances = pd.Series(rf.feature_importances_, index=FEATURE_COLS).sort_values(ascending=False)
    print("\nFeature Importances:")
    print(importances.round(4))

    # ---- Isolation Forest ----
    print("\nTraining Isolation Forest...")
    iso = IsolationForest(n_estimators=100, contamination=0.12, random_state=42)
    iso.fit(X_train_s)

    # Save
    joblib.dump(rf, os.path.join(MODEL_DIR, "mineguard_rf_model.joblib"))
    joblib.dump(iso, os.path.join(MODEL_DIR, "mineguard_iso_model.joblib"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "mineguard_scaler.joblib"))
    joblib.dump(FEATURE_COLS, os.path.join(MODEL_DIR, "feature_cols.joblib"))
    print(f"\nModels saved to {MODEL_DIR}")

if __name__ == "__main__":
    main()
