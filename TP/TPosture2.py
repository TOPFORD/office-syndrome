# Posture2
import cv2
import mediapipe as mp
import time
from PIL import ImageFont, ImageDraw, Image
import numpy as np

# เรียกใช้โมดูล MediaPipe สำหรับตรวจจับท่าทาง
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

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

    # ตรวจจับท่าทาง
    results = pose.process(image)

    # แปลงกลับเป็น BGR เพื่อแสดงผล
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # ตรวจสอบว่ามีจุดท่าทางที่ตรวจจับได้หรือไม่
    if results.pose_landmarks:
        # วาดจุดและเส้นบนร่างกาย
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # ตรวจสอบตำแหน่งของจุดที่เกี่ยวข้องกับท่าที่ต้องการ
        left_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_hand = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        mouth = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT]
        left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]

        # เงื่อนไขสำหรับการตรวจจับท่าทางทั้งด้านซ้ายและขวา
        left_side_correct = (
            
abs(left_elbow.x - mouth.x) < 0.4 and  # ตรวจสอบให้ศอกอยู่ใกล้กับปากในระยะ 0.4
            abs(left_hand.x - mouth.x) < 0.1 and  # ตรวจสอบให้ข้อมืออยู่ใกล้กับปากในระยะ 0.1
            abs(mouth.x - left_shoulder.x) < 0.1  # ตรวจสอบให้ปากอยู่ใกล้ไหล่ซ้าย        )
        )
        right_side_correct = (
            abs(right_elbow.x - mouth.x) < 0.45 and  # ตรวจสอบให้ศอกอยู่ใกล้กับปากในระยะ 0.4
            abs(right_hand.x - mouth.x) < 0.1 and  # ตรวจสอบให้ข้อมืออยู่ใกล้กับปากในระยะ 0.1
            abs(mouth.x - right_shoulder.x) < 0.2  # ตรวจสอบให้ปากอยู่ใกล้ไหล่ขวา
        )

        # ตรวจสอบว่าท่าทางถูกต้องหรือไม่
        if left_side_correct or right_side_correct:
            text = "ท่าทางถูกต้อง"
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= hold_time:
                text = "ท่าทางถูกต้องครบ 10 วินาที"
        else:
            start_time = None
            text = "ท่าที่ 2 ท่าทางไม่ตรงกับที่ต้องการ"
    else:
        start_time = None
        text = "ท่าที่ 2 ท่าทางไม่ตรงกับที่ต้องการ"

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
    cv2.imshow('Pose Detection', image)

    # กด 'q' เพื่อออกจากโปรแกรม
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# ปิดกล้อง
cap.release()
cv2.destroyAllWindows()
