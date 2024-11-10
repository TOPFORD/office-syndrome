import mediapipe as mp

mp_pose = mp.solutions.pose

def check_posture4R(results_pose):
    # ตรวจสอบว่ามี landmarks อยู่หรือไม่
    if not results_pose.pose_landmarks:
        return False  # Return False if landmarks are not available

    # ดึงข้อมูลตำแหน่งของ landmarks สำหรับการตรวจสอบท่าทาง
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]

    left_side_correct = (0.0 < abs(right_elbow.y - right_shoulder.y) < 0.4 and 
                         0.0 < abs(left_hand.x - right_elbow.x) < 0.12)

    return left_side_correct
