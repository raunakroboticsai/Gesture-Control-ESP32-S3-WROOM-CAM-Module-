# Gesture-Control-ESP32-S3-WROOM-CAM-Module-
This project uses ESP32-S3 camera to detect  hand gestures using MediaPipe and controls  a robot car via WiFi. 1 finger = Forward,  2 fingers = Backward, 3 = Left, 4 = Right.

**ESP32-S3 Gesture Control System**

> Real-time hand gesture recognition using ESP32-S3 camera module and MediaPipe — control anything with just your fingers!

![ESP32-S3](https://img.shields.io/badge/ESP32--S3-Gesture%20Control-blue?style=for-the-badge&logo=espressif)
![Python](https://img.shields.io/badge/Python-3.10%2B-green?style=for-the-badge&logo=python)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Landmarks-orange?style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-red?style=for-the-badge&logo=flask)

**-Project Overview**

This project uses an **ESP32-S3-WROOM** camera module to stream live video to a Python server running **MediaPipe Hand Landmark Detection**. The system detects the number of fingers shown to the camera and maps them to directional commands — which can be used to control a robot car, drone, or any other system.

The results are displayed on a **real-time web dashboard** accessible from any browser on the same network.



**Gesture Mapping**

| Gesture | Fingers | Command |
|--------|---------|---------|
| ☝️ One Finger | 1 | **FORWARD** |
| ✌️ Two Fingers | 2 | **BACKWARD** |
| 🤟 Three Fingers | 3 | **LEFT** |
| 🖖 Four Fingers | 4 | **RIGHT** |
| ✊ Fist / No Hand | 0 | **STOP** |

---

**Hardware Required**

| Component | Details |
|-----------|---------|
| ESP32-S3-WROOM | Camera module |
| OV3660 Camera | Onboard camera sensor |
| USB Cable | For programming |
| WiFi Network | ESP32 + PC on same network |

---

**Software Required**

| Software | Version |
|----------|---------|
| Arduino IDE | 2.x |
| ESP32 Board Package | 2.0.x |
| Python | 3.10+ |
| MediaPipe | 0.10.33 |
| OpenCV | Latest |
| Flask | Latest |

---

**Project Structure**

GestureControl-ESP32/
│
├── ESP32_Stream/
│   ├── ESP32_Stream.ino
│   └── camera_pins.h
│
├── gesture_server.py
├── index.html
└── README.md



**Setup & Installation**

**Step 1 — ESP32 Arduino Setup**

1. Open **Arduino IDE**
2. Go to `Tools` and set:
```
   Board          → ESP32S3 Dev Module
   PSRAM          → OPI PSRAM
   Partition      → Huge APP (3MB No OTA/1MB SPIFFS)
   Flash Size     → 8MB
   Upload Speed   → 921600
```
3. Update WiFi credentials in code
4. Upload and note the IP from Serial Monitor

**Step 2 — Python Setup**
```bash
pip install mediapipe==0.10.33 opencv-python flask
```

**Step 3 — Update ESP32 IP**
```python
ESP32_STREAM_URL = "http://192.168.x.x/stream"
```

**Step 4 — Run Server**
```bash
python gesture_server.py
```
**Step 5 — Open Browser**
```
http://localhost:5000
```

**How It Works**

1. ESP32-S3 streams live MJPEG video over WiFi
2. Python reads stream using OpenCV
3. MediaPipe detects 21 hand landmarks
4. Finger count mapped to direction command
5. Flask serves web dashboard with live results



**Author-Raunak Kumar Choudhary**


Made with using ESP32-S3 + MediaPipe(python)
