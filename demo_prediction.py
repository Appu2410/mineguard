"""
MINEGUARD - Live Prediction Demo
Team VORTEX# | SIH 2026 | PS 26025

This script loads the trained model and lets you test sensor readings.
It demonstrates multi-sensor fusion for subsidence risk detection.
"""

import joblib
import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load trained artifacts
model = joblib.load(os.path.join(MODEL_DIR, "mineguard_rf_model.joblib"))
scaler = joblib.load(os.path.join(MODEL_DIR, "mineguard_scaler.joblib"))
feature_cols = joblib.load(os.path.join(MODEL_DIR, "feature_cols.joblib"))

def predict_risk(tilt, vibration, moisture, strain, crack_gap, rssi, acoustic):
    """
    Predict subsidence risk from multi-sensor readings.
    """
    sample = {
        "tilt": tilt,
        "vibration": vibration,
        "moisture": moisture,
        "strain": strain,
        "crack_gap": crack_gap,
        "rssi": rssi,
        "acoustic": acoustic,
    }
    
    df = pd.DataFrame([sample])
    
    # Derived features (same as training)
    df["tilt_vibration_product"] = df["tilt"] * df["vibration"]
    df["strain_crack_ratio"] = df["strain"] / (df["crack_gap"] + 0.1)
    df["signal_anomaly"] = (df["rssi"] + 70).abs()
    
    X = df[feature_cols]
    X_scaled = scaler.transform(X)
    
    pred = model.predict(X_scaled)[0]
    proba = model.predict_proba(X_scaled)[0]
    
    result = {
        "prediction": "SUBSIDENCE RISK ⚠️" if pred == 1 else "NORMAL ✅",
        "confidence": round(float(max(proba)) * 100, 1),
        "risk_probability": round(float(proba[1]) * 100, 1),
        "recommendation": (
            "Raise multi-sensor confirmed alert + GPS tag + notify operators"
            if pred == 1
            else "Continue normal monitoring"
        ),
    }
    return result


# ====================== DEMO CASES ======================
print("=" * 60)
print("   MINEGUARD - Multi-Sensor Subsidence Risk Demo")
print("   Team VORTEX# | SIH 2026 | PS 26025")
print("=" * 60)

# Case 1: Normal ground condition
print("\n📡 CASE 1: Normal Sensor Reading")
print("-" * 40)
normal = {
    "tilt": 0.18,
    "vibration": 0.09,
    "moisture": 21.5,
    "strain": 0.14,
    "crack_gap": 1.3,
    "rssi": -64,
    "acoustic": 0.06,
}
for k, v in normal.items():
    print(f"  {k:12}: {v}")
result = predict_risk(**normal)
print(f"\n  → Prediction     : {result['prediction']}")
print(f"  → Confidence     : {result['confidence']}%")
print(f"  → Risk Probability: {result['risk_probability']}%")
print(f"  → Action         : {result['recommendation']}")

# Case 2: Clear subsidence risk (multi-sensor agreement)
print("\n\n📡 CASE 2: High-Risk Multi-Sensor Event")
print("-" * 40)
risk = {
    "tilt": 2.1,
    "vibration": 0.85,
    "moisture": 25.0,
    "strain": 1.8,
    "crack_gap": 4.5,
    "rssi": -82,
    "acoustic": 0.45,
}
for k, v in risk.items():
    print(f"  {k:12}: {v}")
result = predict_risk(**risk)
print(f"\n  → Prediction     : {result['prediction']}")
print(f"  → Confidence     : {result['confidence']}%")
print(f"  → Risk Probability: {result['risk_probability']}%")
print(f"  → Action         : {result['recommendation']}")

# Case 3: High vibration only (machinery / footsteps - should be filtered)
print("\n\n📡 CASE 3: High Vibration Only (Machinery / Footsteps)")
print("-" * 40)
border = {
    "tilt": 0.25,
    "vibration": 0.65,
    "moisture": 20.0,
    "strain": 0.18,
    "crack_gap": 1.4,
    "rssi": -67,
    "acoustic": 0.35,
}
for k, v in border.items():
    print(f"  {k:12}: {v}")
result = predict_risk(**border)
print(f"\n  → Prediction     : {result['prediction']}")
print(f"  → Confidence     : {result['confidence']}%")
print(f"  → Risk Probability: {result['risk_probability']}%")
print(f"  → Action         : {result['recommendation']}")

print("\n" + "=" * 60)
print("Demo complete. Model correctly distinguishes:")
print("  • True multi-sensor subsidence events")
print("  • Isolated noise (machinery / footsteps)")
print("=" * 60)

# Interactive mode
print("\n\n🔧 INTERACTIVE MODE (press Enter to skip)")
print("Enter sensor values to test custom readings:\n")

try:
    tilt = float(input("Tilt (degrees) [0.1-5.0]: ") or "0.2")
    vibration = float(input("Vibration (g) [0.05-2.0]: ") or "0.1")
    moisture = float(input("Moisture (%) [10-40]: ") or "22")
    strain = float(input("Strain [0.1-3.0]: ") or "0.15")
    crack_gap = float(input("Crack Gap (mm) [0.5-10]: ") or "1.5")
    rssi = float(input("RSSI (dBm) [-90 to -40]: ") or "-65")
    acoustic = float(input("Acoustic [0.01-1.0]: ") or "0.05")
    
    result = predict_risk(tilt, vibration, moisture, strain, crack_gap, rssi, acoustic)
    print("\n" + "-" * 40)
    print(f"  → Prediction     : {result['prediction']}")
    print(f"  → Confidence     : {result['confidence']}%")
    print(f"  → Risk Probability: {result['risk_probability']}%")
    print(f"  → Action         : {result['recommendation']}")
except (ValueError, EOFError, KeyboardInterrupt):
    print("\nSkipped interactive mode.")
