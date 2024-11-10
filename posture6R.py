import mediapipe as mp

mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands

def check_posture6R(results_pose, results_hands, image):
    landmarks = results_pose.pose_landmarks.landmark
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    right_arm_straight = 0 < abs(right_wrist.x - right_shoulder.x) < 0.2 and 0 < abs(right_wrist.x - left_wrist.x) < 0.15

    right_back_of_hand_correct = False
    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            is_back_of_hand = index_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y
            if is_back_of_hand:
                right_back_of_hand_correct = True

    return right_arm_straight and right_back_of_hand_correct
