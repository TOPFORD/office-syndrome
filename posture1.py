import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture1(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    nose = landmarks[mp_pose.PoseLandmark.NOSE]
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_side_correct = (abs(left_elbow.x - left_shoulder.x) < 0.16 and 
                         abs(left_hand.x - mouth.x) < 0.12 and 
                         abs(nose.y - left_shoulder.y) < 0.1)
    
    right_side_correct = (abs(right_elbow.x - right_shoulder.x) < 0.16 and 
                          abs(right_hand.x - mouth.x) < 0.12 and 
                          abs(nose.y - right_shoulder.y) < 0.1)

    return left_side_correct or right_side_correct
