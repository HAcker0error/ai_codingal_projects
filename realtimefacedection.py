import cv2
import os

# Get the folder where this Python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Haar Cascade file located in the same folder
cascade_path = os.path.join(
    BASE_DIR,
    "haarcascade_frontalface_default.xml"
)

# Check if the Haar Cascade file exists
if not os.path.exists(cascade_path):
    print("Error: haarcascade_frontalface_default.xml was not found.")
    print("Expected location:")
    print(cascade_path)
    exit()

# Load the Haar Cascade Classifier
face_cascade = cv2.CascadeClassifier(cascade_path)

# Check if the classifier loaded successfully
if face_cascade.empty():
    print("Error: Could not load the Haar Cascade file.")
    exit()

print("Haar Cascade loaded successfully.")

# Start video capture from camera 1
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Could not open camera 1.")
    print("Trying camera 0...")

    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open any camera.")
    exit()

while True:

    # Capture frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

        cv2.putText(
            frame,
            "Face Detected",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 0, 0),
            2
        )

    # Display the video
    cv2.imshow(
        "Face Detection - Press Q to Quit",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()