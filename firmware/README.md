# MINEGUARD Firmware (ESP32)

This folder contains the embedded-side logic for the 9-node ESP32 mesh.

## Files (planned / stub)

- `gateway_n5.ino` – Gateway node (N5) that performs multi-sensor correlation and raises confirmed alerts.
- `sensor_node.ino` – Standard / precision sensor nodes that read MPU6050, piezo, strain, HC-SR04 and send via ESP-NOW.

## Core Logic (Gateway N5)

```cpp
// Pseudo-code of the confirmation logic running on N5
int active_signals = 0;
if (tilt > 0.10) active_signals++;          // literature attention threshold
if (crack_gap > 2.0) active_signals++;      // literature warning threshold
if (strain > 0.5) active_signals++;
if (vibration > 0.40 && tilt > 0.10) active_signals++;
if (rssi < -75) active_signals++;           // relative movement / drift proxy

if (active_signals >= 3) {
  // Raise CONFIRMED ALERT
  // GPS tag + SMS / local buzzer / dashboard push
}
```

## Notes

- Current prototype decision logic is implemented in the Python ML + threshold layer.
- Full Arduino sketches will be added as the hardware build progresses.
- Future: convert the Random Forest / simple decision rules to TensorFlow Lite Micro for true on-device Edge AI.
