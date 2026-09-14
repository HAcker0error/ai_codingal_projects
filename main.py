import cv2

import cv2

# This always points to the correct location for your installed opencv-python package
cascade_path = r"D:\destop folder\WEBSITE DEVELOPMENT\real time face dection people count\haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascade_path)

# Sanity check — this is the key fix
if face_cascade.empty():
    raise IOError(f"Failed to load cascade classifier from: {cascade_path}")

# Initialize video capture (use webcam)
cap = cv2.VideoCapture(0)  # Use the appropriate camera index for your system
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the count of faces
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, f'People Count: {len(faces)}', (10, 30), font, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Display the frame with face detection and people count
    cv2.imshow('Face Tracking and Counting', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()