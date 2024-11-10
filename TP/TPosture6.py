# Posture6
import cv2
import mediapipe as mp
import time
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# เรียกใช้โมดูล MediaPipe สำหรับตรวจจับท่าทาง
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# เรียกใช้โมดูล MediaPipe Hands สำหรับตรวจจับนิ้วมือ
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# โหลดฟอนต์ภาษาไทย
font_path = "THSarabunNew.ttf"  # กำหนดตำแหน่งไฟล์ฟอนต์
font = ImageFont.truetype(font_path, 32)

# เปิดกล้อง
cap = cv2.VideoCapture(0)

# ตั้งตัวจับเวลา
start_time = None
hold_time = 10  # กำหนดเวลาที่ต้องอยู่ในท่าที่ถูกต้อง (10 วินาที)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # เปลี่ยนสีภาพเป็น RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ตรวจจับท่าทางและนิ้วมือ
    results_pose = pose.process(image)
    results_hands = hands.process(image)

    # แปลงกลับเป็น BGR เพื่อแสดงผล
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # กำหนดค่าเริ่มต้นสำหรับการตรวจสอบ
    left_back_of_hand_correct = False
    right_back_of_hand_correct = False
    text = "ท่าที่ 6 ท่าทางไม่ตรงกับที่ต้องการ"

    # ตรวจสอบว่ามีจุดท่าทางที่ตรวจจับได้หรือไม่
    if results_pose.pose_landmarks:
        # วาดจุดและเส้นบนร่างกาย
        mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # ตรวจสอบตำแหน่งของจุดที่เกี่ยวข้องกับท่าที่ต้องการ
        left_wrist = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_elbow = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_shoulder = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results_pose.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # เงื่อนไขสำหรับการตรวจจับท่าทางทั้งด้านซ้ายและขวา
        left_arm_straight = abs(left_shoulder.y - left_elbow.y) < 0.1 and abs(left_elbow.y - left_wrist.y) < 0.1 or abs(left_shoulder.y - left_elbow.y) < 0.2 and abs(left_elbow.y - left_wrist.y) < 0.2 or abs(left_shoulder.y - left_elbow.y) < 0.3 and abs(left_elbow.y - left_wrist.y) < 0.3
        right_arm_straight = abs(right_shoulder.y - right_elbow.y) < 0.1 and abs(right_elbow.y - right_wrist.y) < 0.1 or abs(right_shoulder.y - right_elbow.y) < 0.2 and abs(right_elbow.y - right_wrist.y) < 0.2 or abs(right_shoulder.y - right_elbow.y) < 0.3 and abs(right_elbow.y - right_wrist.y) < 0.3

    # ตรวจสอบและแสดงผลหลังมือ
    if results_hands.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results_hands.multi_hand_landmarks):
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            # ตรวจสอบว่ามือเป็นหลังมือหรือไม่
            is_back_of_hand = index_tip.y > thumb_tip.y and pinky_tip.y > thumb_tip.y

            # กำหนดให้ตรวจสอบว่ามือซ้ายหรือมือขวาเป็นหลังมือ
            if idx == 0 and is_back_of_hand:
                left_back_of_hand_correct = True
                left_hand_center = (index_tip.x + pinky_tip.x) / 2, (index_tip.y + pinky_tip.y) / 2
            elif idx == 1 and is_back_of_hand:
                right_back_of_hand_correct = True
                right_hand_center = (index_tip.x + pinky_tip.x) / 2, (index_tip.y + pinky_tip.y) / 2

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ตรวจสอบเงื่อนไขว่าท่าทางถูกต้องหรือไม่
    if left_back_of_hand_correct and right_back_of_hand_correct:
        # ตรวจสอบว่ามืออีกข้างอยู่ใกล้กับหลังมือที่เหยียดตรง
        distance_to_left_back = np.sqrt((right_wrist.x - left_hand_center[0]) ** 2 + (right_wrist.y - left_hand_center[1]) ** 2)
        distance_to_right_back = np.sqrt((left_wrist.x - right_hand_center[0]) ** 2 + (left_wrist.y - right_hand_center[1]) ** 2)

        if (left_arm_straight and distance_to_left_back < 0.2 or left_arm_straight and distance_to_left_back < 0.1 or left_arm_straight and distance_to_left_back < 0.3) or (right_arm_straight and distance_to_right_back < 0.2 or right_arm_straight and distance_to_right_back < 0.1 or right_arm_straight and distance_to_right_back < 0.3):
            text = "ท่าทางถูกต้อง"
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= hold_time:
                text = "ท่าทางถูกต้องครบ 10 วินาที"
        else:
            start_time = None  # ตั้งค่าใหม่หากไม่ตรงตามเงื่อนไข
    else:
        start_time = None
        text = "ท่าที่ 6 ท่าทางไม่ตรงกับที่ต้องการ"

    # แสดงข้อความไทยด้วย PIL
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    draw.text((50, 50), text, font=font, fill=(0, 255, 0) if "ท่าทางถูกต้อง" in text else (0, 0, 255))

    # แสดงข้อความแจ้งเวลาที่เหลือ
    if start_time is not None:
        elapsed_time = int(time.time() - start_time)
        draw.text((50, 100), f"อยู่ในท่าที่ถูกต้อง: {elapsed_time}s", font=font, fill=(255, 255, 0))
    
    # แปลงกลับเป็น numpy array
    image = np.array(pil_image)

    # แสดงผลลัพธ์
    cv2.imshow('Pose and Hand Detection', image)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# ปิดกล้อง
cap.release()
cv2.destroyAllWindows()
