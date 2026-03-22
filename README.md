# Gesture-Control-ESP32-S3-WROOM-CAM-Module-
<img width="1600" height="1600" alt="image" src="https://github.com/user-attachments/assets/99bb0d84-cf0e-4479-9551-f8f7f7c4cced" />

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
<img width="1876" height="947" alt="Windowpowershell" src="https://github.com/user-attachments/assets/c17df961-a1f5-47a2-9829-fe65a0991b94" />

**How It Works**

1. ESP32-S3 streams live MJPEG video over WiFi
2. Python reads stream using OpenCV
3. MediaPipe detects 21 hand landmarks
4. Finger count mapped to direction command
5. Flask serves web dashboard with live results

**Live Stream with Landmarks:**
![forward Image 2026-03-21 at 4 44 11 PM](https://github.com/user-attachments/assets/193a0a2c-21ea-49d5-b1a1-4a9773985705)  
![Backward Image 2026-03-21 at 4 44 49 PM](https://github.com/user-attachments/assets/1d1939dd-679a-4a65-bdac-38ff4d5693e6)
![RIGHT Image 2026-03-21 at 4 45 53 PM](https://github.com/user-attachments/assets/b0a4a777-f5f9-4765-af5a-acbe68a78fd9)
![LEFT Image 2026-03-21 at 4 45 18 PM](https://github.com/user-attachments/assets/de55aae4-1ae8-4584-8616-bb1276c2f9c2)
![RIGHT Image 2026-03-21 at 4 45 53 PM](https://github.com/user-attachments/assets/3eeb0b82-cb93-4ca3-8516-caccdd067fe6)
![STOP Image 2026-03-21 at 4 46 27 PM](https://github.com/user-attachments/assets/b487ba94-b2f5-4364-b77a-3c3737c03e3a)




**Author-Raunak Kumar Choudhary**


Made with using ESP32-S3 + MediaPipe(python)
