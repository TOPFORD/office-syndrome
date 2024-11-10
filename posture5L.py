import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture5L(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_thumb = landmarks[mp_pose.PoseLandmark.RIGHT_THUMB]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]

    left_side_correct = (abs(left_shoulder.x - left_elbow.x) < 0.1 and 
                         abs(left_hand.y - right_thumb.y) < 0.2)

    return left_side_correct
