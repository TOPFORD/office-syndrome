import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture5R(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]

    right_side_correct = (abs(right_shoulder.x - right_elbow.x) < 0.1 and 
                          abs(right_hand.y - left_hand.y) < 0.2)

    return right_side_correct
