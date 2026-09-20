# 🛡️ MINEGUARD
### AI-Enabled Low-Cost Real-Time Mine Subsidence Monitoring System

**Team VORTEX#**  
**Smart India Hackathon 2026**  
**Problem Statement:** SIH26025  
**Theme:** Smart Automation | **Category:** Hardware

---

## 📌 Overview

MINEGUARD is a low-cost, AI-powered early warning system for detecting and predicting surface subsidence in underground coal mines.  

It uses a **9-node ESP32 wireless mesh network** with multi-sensor fusion (tilt, vibration, strain, crack gap, RSSI, acoustic) and Edge AI to raise high-confidence alerts only when multiple sensors agree — effectively filtering out noise from machinery and footsteps.

---

## 🎯 Key Features

- 9-Node ESP32 Mesh Network (ESP-NOW)
- Multi-sensor fusion (Tilt + Vibration + Strain + Crack + RSSI)
- Edge AI for real-time anomaly detection
- Local processing + Offline alerts
- GPS tagging of confirmed events
- GIS visualization support
- Low-cost & student-prototype friendly

---

## 📂 Repository Structure

```
mineguard/
├── data/
│   └── mineguard_sensor_dataset.csv      # 5000-sample synthetic dataset
├── models/
│   ├── mineguard_rf_model.joblib         # Random Forest Classifier
│   ├── mineguard_iso_model.joblib        # Isolation Forest
│   ├── mineguard_scaler.joblib           # StandardScaler
│   └── feature_cols.joblib               # Feature list
├── demo_prediction.py                    # Live demo script
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

Synthetic dataset simulating real sensor readings from the 9-node mesh:

| Feature       | Description                          | Sensor              |
|---------------|--------------------------------------|---------------------|
| tilt          | Ground tilt in degrees               | MPU6050             |
| vibration     | Vibration intensity (g)              | Piezoelectric       |
| moisture      | Soil moisture (%)                    | Moisture Sensor     |
| strain        | Strain / deformation                 | Strain Gauge + HX711|
| crack_gap     | Crack width (mm)                     | HC-SR04             |
| rssi          | Signal strength (dBm)                | ESP-NOW             |
| acoustic      | Acoustic emission                    | Piezo               |
| label         | 0 = Normal, 1 = Subsidence Risk      | -                   |

- **Total samples:** 5000  
- **Positive class (risk):** ~12%  
- Includes realistic noise (machinery/footsteps) to test filtering capability.

---

## 🤖 Machine Learning Model

We trained two models:

1. **Random Forest Classifier** (Supervised)  
   - Learns multi-sensor patterns  
   - High confidence only when multiple sensors elevate together

2. **Isolation Forest** (Unsupervised)  
   - Useful for real-world deployment where labeled data is limited

**Key Insight:**  
Isolated high vibration (machinery) is correctly classified as **NORMAL**.  
True risk is raised only on multi-sensor agreement — matching our hardware confirmation logic (≥3 signals).

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/mineguard.git
cd mineguard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the live demo
```bash
python demo_prediction.py
```

You will see three test cases:
- Normal ground condition
- Clear multi-sensor subsidence event
- High vibration only (machinery noise → correctly filtered)

---

## 🖥️ Demo Output Example

```
📡 CASE 2: High-Risk Multi-Sensor Event
  tilt        : 2.1
  vibration   : 0.85
  strain      : 1.8
  crack_gap   : 4.5
  rssi        : -82

  → Prediction     : SUBSIDENCE RISK ⚠️
  → Confidence     : 100.0%
  → Action         : Raise multi-sensor confirmed alert + GPS tag + notify operators
```

---

## 🛠️ Hardware Used (Prototype)

- 9 × ESP32 (Sensor Nodes + Gateway)
- MPU6050 (Tilt / Acceleration)
- Piezoelectric sensor (Vibration + Acoustic)
- Strain Gauge + HX711
- HC-SR04 (Crack gap)
- NEO-6M GPS (Gateway)
- ESP-NOW protocol for mesh communication

---

## 📈 Future Improvements

- Add time-series forecasting (tilt/strain rate of change) for true progression prediction
- Deploy lightweight model on ESP32 gateway using TensorFlow Lite Micro
- Real field data collection & model retraining
- Full GIS dashboard integration

---

## 👥 Team VORTEX#

Smart India Hackathon 2026  
Problem Statement: SIH26025 – Development of an AI-enabled Low Cost Real Time Mine Subsidence Monitoring, Prediction and Early Warning System for Underground Coal Mines in India

---

## 📄 License

This project is developed for Smart India Hackathon 2026.  
Feel free to use for educational and non-commercial purposes.
