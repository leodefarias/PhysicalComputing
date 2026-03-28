import cv2
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(img_gray)

    for face in faces:
        shape = predictor(img_gray, face)
        for i in range(0, 68):
            x = shape.part(i).x
            y = shape.part(i).y
            cv2.circle(frame, (x, y), 2, (255,0,0), -1)
            cv2.putText(frame, str(i), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.7, (0,255,0))

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()