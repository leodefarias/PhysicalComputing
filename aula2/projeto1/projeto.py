import cv2
import mediapipe as mp
import serial
import time
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#Serial
arduino = serial.Serial('COM9', 9600, timeout=1)
time.sleep(2)

#MEDIAPIPE (NOVO)
base_options = python.BaseOptions(
    model_asset_path='hand_landmarker.task'
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    running_mode=vision.RunningMode.VIDEO
)

hands = vision.HandLandmarker.create_from_options(options)

#Leitura da CAM
cap = cv2.VideoCapture(0)
timestamp = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar frame")
        break

    frame = cv2.resize(frame, (500, 500))
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp += 33  # ~30 FPS
    result = hands.detect_for_video(mp_image, timestamp)

    #equivalente ao result.multi_hand_landmarks ===
    if result.hand_landmarks:
        hand_landmarks = result.hand_landmarks[0]

        #dedo indicador (índice 8)
        index_finger_y = hand_landmarks[8].y

        if index_finger_y < 0.5:
            arduino.write(b'1')
        else:
            arduino.write(b'2')

        #(opcional) desenhar pontos simples
        h, w, _ = frame.shape
        for lm in hand_landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

    cv2.imshow("Video", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()