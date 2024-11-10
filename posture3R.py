import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture3R(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    right_side_correct = abs(left_elbow.x - right_shoulder.x) < 0.1

    return right_side_correct
