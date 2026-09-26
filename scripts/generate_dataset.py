"""
MINEGUARD - Synthetic Dataset Generator
Team VORTEX# | SIH 2026 | PS 26025

Generates a realistic multi-sensor dataset for underground coal mine
surface subsidence monitoring.

Thresholds are grounded in published literature:
- Multi-sensor coal mine surface monitoring patent (CN120489061B)
- Tilt-sensor early-warning studies
- Indian coalfield observations (Raniganj, Jharia, Singareni/GDK)

Alert logic: A sample is labelled "risk" only when MULTIPLE sensors
simultaneously exceed literature-based thresholds (matches ≥3-signal
confirmation used on the gateway node N5).
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ============================================================
# LITERATURE-BASED THRESHOLDS (for labelling)
# ============================================================
# Sources:
# 1. CN120489061B – Coal mine multi-sensor real-time monitoring method
#    Yellow: tilt change > 0.1°, crack > 2 mm
#    Orange: tilt > 0.2°, crack > 2–5 mm
#    Red:    tilt > 0.5°, crack > 5 mm
# 2. Tilt sensor array studies (Natural Hazards 2022 and related)
# 3. Indian context rates from Raniganj / Jharia / GDK-11 papers
#    (used for realistic magnitude of events, not direct thresholds)

THRESH = {
    "tilt_attention": 0.10,      # degrees
    "tilt_warning":   0.20,
    "tilt_alert":     0.50,
    "crack_attention": 1.5,      # mm
    "crack_warning":   2.0,
    "crack_alert":     5.0,
    "strain_attention": 0.5,     # relative / micro-strain proxy
    "strain_warning":   1.0,
    "vibration_high":   0.40,    # g  (machinery can exceed this alone)
    "rssi_degrade":   -75,       # dBm (signal drift / relative movement proxy)
}

def is_risk_event(tilt, crack_gap, strain, vibration, rssi):
    """
    Multi-sensor confirmation logic (mirrors N5 gateway).
    Returns True only if ≥3 sensors indicate anomalous movement.
    Isolated high vibration (machinery/footsteps) is NOT labelled risk.
    """
    signals = 0
    if tilt >= THRESH["tilt_attention"]:
        signals += 1
    if crack_gap >= THRESH["crack_warning"]:
        signals += 1
    if strain >= THRESH["strain_attention"]:
        signals += 1
    if vibration >= THRESH["vibration_high"] and tilt >= THRESH["tilt_attention"]:
        # vibration only counts when accompanied by tilt (true ground movement)
        signals += 1
    if rssi <= THRESH["rssi_degrade"]:
        signals += 1
    return signals >= 3


def generate_dataset(n_samples=5000, n_nodes=9):
    start_time = datetime(2026, 1, 1)
    timestamps = [start_time + timedelta(minutes=i * 5) for i in range(n_samples)]

    data = {
        "timestamp": timestamps,
        "node_id": np.random.randint(1, n_nodes + 1, n_samples),
    }

    # ---- Normal operating conditions ----
    data["tilt"] = np.random.normal(0.12, 0.06, n_samples)          # deg
    data["vibration"] = np.random.normal(0.08, 0.04, n_samples)     # g
    data["moisture"] = np.random.normal(22.0, 4.0, n_samples)       # %
    data["strain"] = np.random.normal(0.15, 0.06, n_samples)        # proxy
    data["crack_gap"] = np.random.normal(1.1, 0.35, n_samples)      # mm
    data["rssi"] = np.random.normal(-64, 5, n_samples)              # dBm
    data["acoustic"] = np.random.normal(0.05, 0.025, n_samples)

    # ---- Inject true subsidence events (~12%) ----
    # Magnitudes inspired by observed rates in Indian coalfields
    # (Raniganj DGPS up to ~117 mm/yr local; InSAR cm-level zones)
    n_events = int(0.12 * n_samples)
    event_idx = np.random.choice(n_samples, size=n_events, replace=False)

    for idx in event_idx:
        severity = np.random.uniform(1.2, 3.5)
        data["tilt"][idx] += severity * np.random.uniform(0.25, 0.9)
        data["strain"][idx] += severity * np.random.uniform(0.4, 1.2)
        data["crack_gap"][idx] += severity * np.random.uniform(1.0, 3.5)
        data["vibration"][idx] += severity * np.random.uniform(0.15, 0.45)
        data["rssi"][idx] -= severity * np.random.uniform(6, 18)
        data["acoustic"][idx] += severity * np.random.uniform(0.08, 0.35)
        data["moisture"][idx] += np.random.uniform(-4, 6)

    # ---- Inject isolated noise (machinery / footsteps) ----
    # High vibration only – should NOT be labelled risk
    noise_idx = np.random.choice(
        np.setdiff1d(np.arange(n_samples), event_idx), size=250, replace=False
    )
    for idx in noise_idx:
        data["vibration"][idx] += np.random.uniform(0.35, 0.9)
        data["acoustic"][idx] += np.random.uniform(0.15, 0.4)

    # Clip to realistic physical ranges
    data["tilt"] = np.clip(data["tilt"], 0, 6)
    data["vibration"] = np.clip(data["vibration"], 0, 2.5)
    data["moisture"] = np.clip(data["moisture"], 5, 45)
    data["strain"] = np.clip(data["strain"], 0, 5)
    data["crack_gap"] = np.clip(data["crack_gap"], 0.4, 12)
    data["rssi"] = np.clip(data["rssi"], -95, -35)
    data["acoustic"] = np.clip(data["acoustic"], 0, 1.5)

    df = pd.DataFrame(data)

    # Label using multi-sensor literature thresholds
    labels = []
    for i in range(len(df)):
        labels.append(
            1 if is_risk_event(
                df.loc[i, "tilt"],
                df.loc[i, "crack_gap"],
                df.loc[i, "strain"],
                df.loc[i, "vibration"],
                df.loc[i, "rssi"],
            )
            else 0
        )
    df["label"] = labels

    # Derived features (same as used in training)
    df["tilt_vibration_product"] = df["tilt"] * df["vibration"]
    df["strain_crack_ratio"] = df["strain"] / (df["crack_gap"] + 0.1)
    df["signal_anomaly"] = (df["rssi"] + 70).abs()

    return df


if __name__ == "__main__":
    print("Generating MINEGUARD dataset with literature-based thresholds...")
    df = generate_dataset(n_samples=5000)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "mineguard_sensor_dataset.csv")
    df.to_csv(out_path, index=False)

    print(f"Saved: {out_path}")
    print(f"Shape: {df.shape}")
    print(f"Label distribution:\n{df['label'].value_counts()}")
    print("\nThresholds used for labelling:")
    for k, v in THRESH.items():
        print(f"  {k}: {v}")
    print("\nDone.")
