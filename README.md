# 🛡️ MINEGUARD
### AI-Enabled Low-Cost Real-Time Mine Subsidence Monitoring System

**Team VORTEX#**  
**Smart India Hackathon 2026** | **PS 26025**  
**Theme:** Smart Automation | **Category:** Hardware  
**Organization:** Ministry of Coal / Coal India Limited

---

## 📌 Overview

MINEGUARD is a low-cost, AI-powered early-warning system for detecting surface subsidence above underground coal mines in India.  

It uses a **9-node ESP32 wireless mesh** with multi-sensor fusion (tilt, vibration, strain, crack gap, RSSI, acoustic).  
The gateway node (N5) raises a **confirmed alert only when ≥3 sensors agree**, filtering out false alarms from machinery, footsteps and blasting.

---

## 🎯 Key Design Decision

> **Multi-sensor confirmation (≥3 signals)** is the core innovation.  
> Isolated high vibration (machinery) is ignored. True ground movement produces concurrent changes in tilt + strain + crack + signal drift.

This logic is implemented both in:
- The gateway firmware stub (`firmware/`)
- The Python ML + threshold labelling pipeline

---

## 📐 Literature-Based Thresholds

Alert labels in the dataset and the decision logic are **not arbitrary**.  
They are derived from published multi-sensor coal-mine monitoring studies and adapted to our low-cost surface mesh.

| Parameter              | Attention     | Warning       | Alert / Danger | Primary Source |
|------------------------|---------------|---------------|----------------|----------------|
| **Tilt change**        | > 0.10°      | > 0.20°      | > 0.50°       | CN120489061B + tilt-sensor EWS literature |
| **Crack widening**     | > 1.5 mm     | > 2.0 mm     | > 5.0 mm      | CN120489061B |
| **Strain (proxy)**     | > 0.5        | > 1.0        | –             | Mining strain literature + multi-sensor fusion papers |
| **Vibration**          | –            | High only when accompanied by tilt | – | Filtering design (machinery rejection) |
| **RSSI / signal drift**| < –75 dBm   | –            | –             | Proxy for relative node movement |

**Indian coalfield context** (used for realistic event magnitudes):
- Raniganj coalfield – InSAR + DGPS studies (max local rates observed up to ~117 mm/year at critical points)
- Jharia coalfield – multi-sensor remote sensing of fire-induced subsidence
- GDK-11 (Singareni) – PS-InSAR monitoring of continuous-miner caving panels

References are listed at the end of this README.

---

## 📂 Repository Structure

```
mineguard/
├── data/
│   └── mineguard_sensor_dataset.csv     # 5000 samples, literature-threshold labelled
├── models/
│   ├── mineguard_rf_model.joblib        # Random Forest
│   ├── mineguard_iso_model.joblib       # Isolation Forest
│   ├── mineguard_scaler.joblib
│   └── feature_cols.joblib
├── scripts/
│   ├── generate_dataset.py              # How the synthetic data + labels are created
│   └── train_model.py                   # Full training + feature importance
├── firmware/
│   ├── README.md
│   └── gateway_n5_stub.ino              # ESP32 gateway confirmation logic stub
├── demo_prediction.py                   # Live demo
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/appu2410/mineguard.git
cd mineguard
pip install -r requirements.txt
python demo_prediction.py
```

To regenerate everything from scratch:

```bash
python scripts/generate_dataset.py
python scripts/train_model.py
```

---

## 🤖 Models

1. **Random Forest Classifier** (supervised) – primary demo model  
2. **Isolation Forest** (unsupervised) – useful when labelled field data is scarce

Both use the same feature set. Feature importance consistently ranks **strain, crack_gap and tilt** highest — matching the physical expectation for subsidence.

**Edge AI note:**  
Current models run in the Python prototype / gateway companion.  
Field deployment path: convert the decision rules or a distilled tree to **TensorFlow Lite Micro** on the ESP32 gateway (listed under Future Work).

---

## 🛠️ Hardware (Prototype)

- 9 × ESP32 (mesh nodes + N5 gateway)
- MPU6050 – tilt / acceleration
- Piezoelectric sensor – vibration + acoustic emission
- Strain gauge + HX711
- HC-SR04 – crack gap
- NEO-6M GPS (gateway only)
- ESP-NOW mesh communication

---

## 📈 Future Work

- Complete Arduino sensor drivers and full ESP-NOW mesh
- TensorFlow Lite Micro port of the confirmation logic / lightweight model
- Field calibration at a Coal India / SCCL site
- GIS dashboard with live risk zones

---

## 📚 Key References

**Threshold & multi-sensor systems**
1. CN120489061B – Coal mine area earth surface subsidence real-time monitoring method integrating multiple sensors (multi-level tilt & crack thresholds).
2. Risk evaluation and warning threshold of unstable slope using tilting sensor array. *Natural Hazards*, 2022.  
   https://link.springer.com/article/10.1007/s11069-022-05383-y

**Indian coalfield studies**
3. Surface deformation monitoring of Raniganj coalfield, India, using advanced InSAR and DGPS. *Geomatics, Natural Hazards and Risk*, 2024.  
   https://doi.org/10.1080/19475705.2024.2375546
4. Monitoring of Subsidence Over Continuous Miner-Based Coal Mine Caving Panels Using PS-InSAR Technique (GDK-11, India). *Mining, Metallurgy & Exploration*, 2023.  
   https://link.springer.com/article/10.1007/s42461-023-00744-y
5. Detecting, mapping and monitoring of land subsidence in Jharia Coalfield… *Journal of Earth System Science*, 2015.
6. Subsidence monitoring techniques in coal mining: Indian scenario. *Indian Journal of Geo-Marine Sciences*, 2018.  
   http://nopr.niscpr.res.in/handle/123456789/45170

---

## 👥 Team VORTEX#

Smart India Hackathon 2026  
Problem Statement SIH26025 – Development of an AI-enabled Low Cost Real Time Mine Subsidence Monitoring, Prediction and Early Warning System for Underground Coal Mines in India

---

## License

Developed for Smart India Hackathon 2026.  
MIT License – free for educational and non-commercial use.
