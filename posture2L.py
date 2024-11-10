import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture2L(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]

    left_side_correct = (abs(left_elbow.x - mouth.x) < 0.4 and  
                         abs(left_hand.x - mouth.x) < 0.1 and  
                         abs(mouth.x - left_shoulder.x) < 0.1)

    return left_side_correct
