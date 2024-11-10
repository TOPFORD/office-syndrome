import cv2
import mediapipe as mp

# Initialize MediaPipe Pose and OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)  # เปิดกล้อง (0) คือกล้องหลักของคอมพิวเตอร์

def check_posture6(results_pose):
    if not results_pose.pose_landmarks:
        return False  # Return False if landmarks are not available

    landmarks = results_pose.pose_landmarks.landmark
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]

    left_side_correct = (0 < abs(left_elbow.y - left_shoulder.y) < 0.4 and 
                         0 < abs(right_hand.x - left_elbow.x) < 0.12)

    return left_side_correct

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror view
    frame = cv2.flip(frame, 1)
    
    # Convert the frame color to RGB for Mediapipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(rgb_frame)

    # Draw landmarks for both arms if available
    if results_pose.pose_landmarks:
        landmarks = results_pose.pose_landmarks.landmark

        # Define positions for left and right arm landmarks
        left_elbow_pos = (int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * frame.shape[1]),
                          int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * frame.shape[0]))
        left_shoulder_pos = (int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * frame.shape[1]),
                             int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * frame.shape[0]))

        right_wrist_pos = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * frame.shape[1]),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * frame.shape[0]))
        right_elbow_pos = (int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * frame.shape[1]),
                           int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * frame.shape[0]))
        right_shoulder_pos = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * frame.shape[1]),
                              int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * frame.shape[0]))

        # Draw circles on landmarks for left arm
        cv2.circle(frame, left_elbow_pos, 10, (255, 0, 0), -1)  # Left elbow
        cv2.circle(frame, left_shoulder_pos, 10, (0, 0, 255), -1)  # Left shoulder

        # Draw lines connecting left arm landmarks
        cv2.line(frame, left_shoulder_pos, left_elbow_pos, (255, 255, 255), 2)

        # Draw circles on landmarks for right arm
        cv2.circle(frame, right_wrist_pos, 10, (0, 255, 255), -1)  # Right wrist
        cv2.circle(frame, right_elbow_pos, 10, (255, 0, 255), -1)  # Right elbow
        cv2.circle(frame, right_shoulder_pos, 10, (255, 255, 0), -1)  # Right shoulder

        # Draw lines connecting right arm landmarks
        cv2.line(frame, right_shoulder_pos, right_elbow_pos, (255, 255, 255), 2)
        cv2.line(frame, right_elbow_pos, right_wrist_pos, (255, 255, 255), 2)

    # Check posture
    if check_posture6(results_pose):
        cv2.putText(frame, 'Posture Correct', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(frame, 'Adjust Posture', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display the frame
    cv2.imshow("Posture Detection", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
