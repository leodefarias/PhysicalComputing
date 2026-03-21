import cv2
import mediapipe as mp
import serial
import time

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

arduino = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

base_options = python.BaseOptions(model_asset_path="face_landmarker.task")

options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    num_faces=1
)

detector = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

piscadas = 0
frames_fechado = 0

LIMIAR_FECHAR = 0.38
LIMIAR_ABRIR = 0.42
LIMIAR_COCHILO = 30

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    resultado = detector.detect(mp_image)

    if resultado.face_landmarks:

        pontos = resultado.face_landmarks[0]

        for p in pontos:
            x = int(p.x * frame.shape[1])
            y = int(p.y * frame.shape[0])
            cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        h = abs(pontos[33].x - pontos[133].x)
        v1 = abs(pontos[159].y - pontos[145].y)
        v2 = abs(pontos[158].y - pontos[153].y)

        ear = (v1 + v2) / (2.0 * h)

        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        if ear <= LIMIAR_FECHAR:

            frames_fechado += 1

            if frames_fechado == 3:
                piscadas += 1
                arduino.write(b'G')

            elif frames_fechado > LIMIAR_COCHILO:
                arduino.write(b'R')

        elif ear > LIMIAR_ABRIR:

            frames_fechado = 0
            arduino.write(b'G')

        cv2.putText(frame, f"PISCADAS: {piscadas}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Detector de Fadiga", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()