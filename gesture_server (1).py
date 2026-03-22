import cv2
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision
import numpy as np
from flask import Flask, Response, jsonify
import threading
import time
import os
import urllib.request as req_lib

# ===========================
# CHANGE THIS TO YOUR ESP32 IP
# ===========================
ESP32_STREAM_URL = "http://192.168.137.168/stream"

# ===========================
# Flask App
# ===========================
app = Flask(__name__)

current_fingers   = 0
current_direction = "STOP"
current_frame     = None
frame_lock        = threading.Lock()

# ===========================
# Download model
# ===========================
MODEL_PATH = "hand_landmarker.task"
MODEL_URL  = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"

def download_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading MediaPipe hand model... (one time only)")
        req_lib.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded!")
    else:
        print("Model already exists!")

# ===========================
# Finger Counting
# ===========================
FINGER_TIPS = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers_up = 0
    lm = hand_landmarks
    if lm[FINGER_TIPS[0]].x < lm[FINGER_TIPS[0] - 1].x:
        fingers_up += 1
    for tip_id in FINGER_TIPS[1:]:
        if lm[tip_id].y < lm[tip_id - 2].y:
            fingers_up += 1
    return fingers_up

def get_direction(f):
    if f == 1: return "FORWARD"
    if f == 2: return "BACKWARD"
    if f == 3: return "LEFT"
    if f == 4: return "RIGHT"
    return "STOP"

DIR_COLORS = {
    "FORWARD":  (0, 255, 136),
    "BACKWARD": (51, 51, 255),
    "LEFT":     (0, 204, 255),
    "RIGHT":    (255, 204, 0),
    "STOP":     (255, 255, 255),
}

HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]

def draw_landmarks(frame, landmarks, w, h):
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 180, 180), 2)
    for pt in pts:
        cv2.circle(frame, pt, 5, (0, 245, 255), -1)

# ===========================
# Main Stream Thread
# ===========================
def read_esp32_stream():
    global current_fingers, current_direction, current_frame

    download_model()

    # MediaPipe setup
    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.IMAGE,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5
    )
    detector = vision.HandLandmarker.create_from_options(options)

    while True:
        print(f"Connecting to ESP32: {ESP32_STREAM_URL}")
        
        # OpenCV VideoCapture — most stable for MJPEG streams
        cap = cv2.VideoCapture(ESP32_STREAM_URL)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimum buffer — always latest frame

        if not cap.isOpened():
            print("Cannot connect! Retrying in 3s...")
            time.sleep(3)
            continue

        print("ESP32 Connected! Reading frames...")

        while True:
            ret, frame = cap.read()

            if not ret or frame is None:
                print("Frame lost! Reconnecting...")
                break  # Reconnect

            # Flip horizontally
            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]

            # MediaPipe detection
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            result = detector.detect(mp_image)

            fingers = 0
            if result.hand_landmarks:
                for hand_lm in result.hand_landmarks:
                    draw_landmarks(frame, hand_lm, w, h)
                    fingers = count_fingers(hand_lm)

            direction = get_direction(fingers)
            current_fingers   = fingers
            current_direction = direction

            # Draw UI overlay
            color = DIR_COLORS.get(direction, (255, 255, 255))
            cv2.rectangle(frame, (0, 0), (w, 55), (0, 0, 0), -1)
            cv2.rectangle(frame, (0, 0), (w, 55), color, 2)
            cv2.putText(frame, direction, (10, 40),
                        cv2.FONT_HERSHEY_DUPLEX, 1.1, color, 2)
            cv2.putText(frame, f"Fingers: {fingers}", (w - 155, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            # Save frame for web
            with frame_lock:
                _, jpeg = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                current_frame = jpeg.tobytes()

        cap.release()
        time.sleep(2)  # Wait before reconnect

# ===========================
# Flask Routes
# ===========================
def generate_frames():
    while True:
        with frame_lock:
            frame = current_frame
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)

@app.route('/')
def index():
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/gesture')
def gesture():
    return jsonify({
        "fingers":   current_fingers,
        "direction": current_direction
    })

# ===========================
# Main
# ===========================
if __name__ == '__main__':
    t = threading.Thread(target=read_esp32_stream, daemon=True)
    t.start()

    print("\n" + "="*50)
    print("  GESTURE CONTROL SERVER STARTED!")
    print("="*50)
    print(f"  ESP32 Stream : {ESP32_STREAM_URL}")
    print(f"  Web Page     : http://localhost:5000")
    print("="*50 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
