import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture4L(results_pose):
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