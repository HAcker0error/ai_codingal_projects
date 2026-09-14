import cv2
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

cascade_path = os.path.join(BASE_DIR,"haarcascade_frontalface_default.xml")

if not os.path.exists(cascade_path):
    print("Error: haarcascade_frontalface_default.xml was not found.")
    print("Expected location:")
    print(cascade_path)
    exit()

face_cascade = cv2.CascadeClassifier(cascade_path)

if face_cascade.empty():
    print("Error: Could not load the Haar Cascade file.")
    exit()

print("Haar Cascade loaded successfully.")

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open camera 1.")
    print("Trying camera 0...")

    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open any camera.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame,(x, y),(x + w, y + h),(255, 0, 0), 2)
        cv2.putText(frame,"Face Detected",(x, y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255, 0, 0),2)


    cv2.imshow("Face Detection - Press Q to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()