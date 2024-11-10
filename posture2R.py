import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture2R(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    right_side_correct = (abs(right_elbow.x - mouth.x) < 0.45 and
                          abs(right_hand.x - mouth.x) < 0.1 and
                          abs(mouth.x - right_shoulder.x) < 0.2)

    return right_side_correct
