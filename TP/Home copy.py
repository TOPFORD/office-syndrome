import cv2
import mediapipe as mp
import time
from PIL import ImageFont, ImageDraw, Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import ttk
import pygame  # นำเข้า pygame สำหรับเสียงแจ้งเตือน

# เรียกใช้โมดูล MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# โหลดฟอนต์ภาษาไทย
font_path = "THSarabunNew.ttf"
font = ImageFont.truetype(font_path, 32)

# เริ่ม pygame สำหรับเล่นเสียง
pygame.init()
alert_sound = pygame.mixer.Sound("Audio.MP3")  # โหลดเสียงแจ้งเตือน (กรุณาเปลี่ยนเป็นไฟล์เสียงที่คุณมี)

# กำหนดเวลาถือท่า
hold_time = 5
start_time = None
is_running = False
current_pose = 1
target_repeats = 2  # ค่าเริ่มต้นเป็น 2 ครั้ง
current_repeats = 0

# จำนวนครั้งที่ทำสำหรับแต่ละท่า
pose_counts = [0] * 6  # จำนวนครั้งที่ทำสำหรับท่าทั้ง 6

# ฟังก์ชันตรวจสอบท่าทางที่ 1
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

# ฟังก์ชันตรวจสอบท่าทางที่ 2
def check_posture2(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_side_correct = (abs(left_elbow.x - mouth.x) < 0.4 and 
                         abs(left_hand.x - mouth.x) < 0.1 and 
                         abs(mouth.x - left_shoulder.x) < 0.1)
    
    right_side_correct = (abs(right_elbow.x - mouth.x) < 0.45 and 
                          abs(right_hand.x - mouth.x) < 0.1 and 
                          abs(mouth.x - right_shoulder.x) < 0.2)

    return left_side_correct or right_side_correct

# ฟังก์ชันตรวจสอบท่าทางที่ 3
def check_posture3(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_side_correct = abs(right_elbow.x - left_shoulder.x) < 0.1
    right_side_correct = abs(left_elbow.x - right_shoulder.x) < 0.1

    return left_side_correct or right_side_correct

# ฟังก์ชันตรวจสอบท่าทางที่ 4
def check_posture4(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_side_correct = (abs(left_elbow.y > left_shoulder.y) < 0.4 and 
                         abs(left_hand.x - right_shoulder.x) < 0.1 and 
                         abs(left_shoulder.y < right_elbow.y) and 
                         abs(left_shoulder.x - right_elbow.x) < 1)
    
    right_side_correct = (abs(right_elbow.y > right_shoulder.y) < 0.4 and 
                          abs(right_hand.x - left_shoulder.x) < 0.1 and 
                          abs(right_shoulder.y < left_elbow.y) and 
                          abs(right_shoulder.x - left_elbow.x) < 1)

    return left_side_correct or right_side_correct

# ฟังก์ชันตรวจสอบท่าทางที่ 5
def check_posture5(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_hand = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_hand = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    right_thumb = landmarks[mp_pose.PoseLandmark.RIGHT_THUMB]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_side_correct = abs(left_shoulder.x - left_hand.x) < 0.1 and abs(left_hand.y - right_thumb.y) < 0.2
    right_side_correct = abs(right_shoulder.x - right_hand.x) < 0.1 and abs(right_hand.y - left_hand.y) < 0.2

    return left_side_correct or right_side_correct

# ฟังก์ชันตรวจสอบท่าทางที่ 6
def check_posture6(results_pose):
    landmarks = results_pose.pose_landmarks.landmark
    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

    left_arm_straight = abs(left_shoulder.y - left_elbow.y) < 0.3 and abs(left_elbow.y - left_wrist.y) < 0.3
    right_arm_straight = abs(right_shoulder.y - right_elbow.y) < 0.3 and abs(right_elbow.y - right_wrist.y) < 0.3

    return left_arm_straight and right_arm_straight

# แมพตำแหน่งท่ากับฟังก์ชันตรวจสอบท่าที่เหมาะสม
posture_checks = [check_posture1, check_posture2, check_posture3, check_posture4, check_posture5, check_posture6]

# ฟังก์ชันการทำงานของกล้อง
def start_pose_detection():
    global is_running, start_time, current_repeats
    is_running = True
    start_time = None
    current_repeats = 0
    update_frame()

def stop_pose_detection():
    global is_running
    is_running = False

def restart_pose_detection():
    global current_pose, start_time, current_repeats
    current_pose = 1
    start_time = None
    current_repeats = 0
    status_label.config(text="")  # เคลียร์สถานะ
    start_pose_detection()

def select_repeats(value):
    global target_repeats
    target_repeats = int(value)

def update_frame():
    global start_time, is_running, current_pose, current_repeats
    if not is_running:
        return

    # กำหนดค่าเริ่มต้นให้กับ text เพื่อป้องกันข้อผิดพลาด
    text = f"ท่าที่ {current_pose} ท่าทางไม่ตรงกับที่ต้องการ"

    success, frame = cap.read()
    if not success:
        return

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results_pose.pose_landmarks:
        mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        posture_check = posture_checks[current_pose - 1]
        is_correct_pose = posture_check(results_pose)

        if is_correct_pose:
            if start_time is None:
                start_time = time.time()
            elif time.time() - start_time >= hold_time:
                alert_sound.play()  # เล่นเสียงแจ้งเตือน
                text = f"ท่าที่ {current_pose} ถูกต้องครบ 10 วินาที (ครั้งที่ {current_repeats + 1}/{target_repeats})"
                start_time = None
                current_repeats += 1

                # ตรวจสอบว่าทำครบจำนวนครั้งที่กำหนดหรือยัง
                if current_repeats >= target_repeats:
                    status_label.config(text=f"ท่าที่ {current_pose} ผ่านแล้ว!")  # แสดงข้อความว่า ผ่าน
                    current_pose += 1
                    current_repeats = 0
                    if current_pose > len(posture_checks):
                        current_pose = 1
                        status_label.config(text="ทำท่าครบทุกท่าแล้ว!")  # แสดงข้อความว่า ทำครบทุกท่าแล้ว
        else:
            start_time = None
    else:
        start_time = None

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    draw.text((50, 50), text, font=font, fill=(0, 255, 0) if "ท่าทางถูกต้อง" in text else (0, 0, 255))

    if start_time is not None:
        elapsed_time = int(time.time() - start_time)
        draw.text((50, 100), f"อยู่ในท่าที่ถูกต้อง: {elapsed_time}s", font=font, fill=(255, 255, 0))

    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(image))
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    window.after(10, update_frame)

# สร้างหน้าต่าง UI
window = tk.Tk()
window.title("Pose Detection")
window.geometry("800x600")

# แสดงกล้อง
video_label = tk.Label(window)
video_label.pack()

# สร้างปุ่มควบคุม
control_frame = tk.Frame(window)
control_frame.pack(pady=10)

start_button = tk.Button(control_frame, text="เริ่ม", command=start_pose_detection)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(control_frame, text="หยุด", command=stop_pose_detection)
stop_button.grid(row=0, column=1, padx=5)

restart_button = tk.Button(control_frame, text="รีสตาร์ท", command=restart_pose_detection)
restart_button.grid(row=0, column=2, padx=5)

# เพิ่ม Label สำหรับช่องจำนวนครั้ง
repeat_label = tk.Label(control_frame, text="จำนวนครั้งที่ต้องทำ")
repeat_label.grid(row=0, column=3, padx=5)

# สร้าง Combobox สำหรับเลือกจำนวนครั้งในการทำท่า
repeat_selector = ttk.Combobox(control_frame, values=[2, 3], state="readonly")
repeat_selector.set(2)  # ค่าเริ่มต้นเป็น 2 ครั้ง
repeat_selector.grid(row=0, column=4, padx=5)
repeat_selector.bind("<<ComboboxSelected>>", lambda e: select_repeats(repeat_selector.get()))

# สร้าง Label สำหรับแสดงสถานะการทำท่า
status_label = tk.Label(window, text="", font=("THSarabunNew", 16), justify="left")
status_label.pack(pady=10)

# เริ่มต้นการใช้งานกล้อง
cap = cv2.VideoCapture(0)

window.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), window.destroy()])
window.mainloop()
