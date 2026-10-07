import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

print("Hand Tracking Started! Press 'q' to quit.")

def detect_gesture(hand_landmarks):
    landmarks = hand_landmarks.landmark
    thumb_points = [4, 3]
    finger_points = [(8, 6), (12, 10), (16, 14), (20, 18)]
    fingers = 0

    if landmarks[thumb_points[0]].y < landmarks[thumb_points[1]].y:
        thumb = "Up"
    else:
        thumb = "Down"

    for tip, pip in finger_points:
        if landmarks[tip].y < landmarks[pip].y:
            fingers += 1

    if thumb == "Up" and fingers == 0:
        return "Thumbs Up"
    elif thumb == "Down" and fingers == 0:
        return "Thumbs Down"
    elif fingers == 4:
        return "Open"
    elif fingers == 0:
        return "Closed Fist"
    elif fingers == 2:
        return "Peace"
    else:
        return "Unknown"

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    gesture = "No hand detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            gesture = detect_gesture(hand_landmarks)
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.putText(frame, f"Gesture: {gesture}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Gesture Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()