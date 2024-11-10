import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture3L(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

    left_side_correct = abs(right_elbow.x - left_shoulder.x) < 0.1

    return left_side_correct
