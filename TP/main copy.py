import cv2
import mediapipe as mp
from PIL import ImageFont, ImageDraw, Image, ImageTk
import numpy as np
import tkinter as tk
from tkinter import ttk
import pygame
from completion_timer import CompletionTimer  # นำเข้า CompletionTimer
import time


# นำเข้าฟังก์ชันตรวจสอบท่าทางจากไฟล์แยกต่างหาก
from posture1 import check_posture1
from posture2L import check_posture2
from posture2R import check_posture3
from posture3L import check_posture4
from posture3R import check_posture5
from posture4L import check_posture6
from posture4R import check_posture7
from posture5L import check_posture8
from posture5R import check_posture9
from posture6L import check_posture10
from posture6R import check_posture11

# สร้างรายการ posture_checks เพื่อเชื่อมโยงกับฟังก์ชันแต่ละท่าทาง
posture_checks = [
    check_posture1,
    check_posture2,
    check_posture3,
    check_posture4,
    check_posture5,
    check_posture6,
    check_posture7,
    check_posture8,
    check_posture9,
    check_posture10,
    check_posture11
]

# Initialize MediaPipe and pygame
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load Thai font and alert sound
font_path = "THSarabunNew.ttf"
font = ImageFont.truetype(font_path, 32)
pygame.init()
alert_sound = pygame.mixer.Sound("Audio.MP3")

# Set initial states
start_time = None
current_pose = 1
target_repeats = 2
current_repeats = 0
completed_time = None

def select_repeats(value):
    global target_repeats
    target_repeats = int(value)


# ฟังก์ชัน track_pose ย้ายมาจาก pose_tracker.py
def track_pose(posture_check, results_pose, results_hands, image, current_pose, target_repeats, start_time, current_repeats):
    """
    ตรวจสอบว่าท่าทางถูกต้องหรือไม่และนับจำนวนครั้งที่ทำสำเร็จ
    """
    is_correct_pose = False
    if current_pose in [10, 11]:  # ท่าที่ 10 และ 11 ใช้การตรวจสอบมือด้วย
        is_correct_pose = posture_check(results_pose, results_hands, image)
    else:
        is_correct_pose = posture_check(results_pose)

    # หากท่าทางถูกต้อง เริ่มจับเวลา
    if is_correct_pose:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= 2:
            alert_sound.play()
            start_time = None
            current_repeats += 1

            # ตรวจสอบว่าทำท่าครบตามจำนวนที่ตั้งไว้หรือยัง
            if current_repeats >= target_repeats:
                return True, start_time, current_repeats  # ทำครบแล้ว
    else:
        start_time = None  # รีเซ็ตเวลาเริ่มต้นหากทำท่าผิด

    return False, start_time, current_repeats

def start_completion_timer():
    """เรียกใช้ CompletionTimer เมื่อทำท่าครบ"""
    completion_timer = CompletionTimer(countdown_time=5)  # ตั้งเวลา 5 วินาที
    window.destroy()  # ปิดหน้าต่าง Tkinter
    completion_timer.start_and_restart()  # เริ่มนับถอยหลังและรันโปรแกรมใหม่

# Function to start, stop pose detection
def start_pose_detection():
    global is_running, start_time, current_repeats, completed_time
    is_running = True
    start_time = None
    current_repeats = 0
    completed_time = None
    update_frame()

def stop_pose_detection():
    global is_running
    is_running = False

def update_frame():
    global start_time, is_running, current_pose, current_repeats, completed_time
    if not is_running:
        return

    text = f"ท่าที่ {current_pose} ท่าทางไม่ตรงกับที่ต้องการ"

    success, frame = cap.read()
    if not success:
        return

    frame = cv2.resize(frame, (screen_width, screen_height))
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(image)
    results_hands = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results_pose.pose_landmarks:
        mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        posture_check = posture_checks[current_pose - 1]
        
        # ตรวจสอบท่าทางและนับจำนวนครั้งที่ทำสำเร็จ
        pose_complete, start_time, current_repeats = track_pose(
            posture_check, results_pose, results_hands, image, current_pose, target_repeats, start_time, current_repeats
        )

        if pose_complete:
            status_label.config(text=f"ท่าที่ {current_pose} ผ่านแล้ว!")
            current_pose += 1
            current_repeats = 0
            if current_pose > len(posture_checks):  # ทำครบทุกท่าแล้ว
                status_label.config(text="ทำท่าครบทุกท่าแล้ว! ปิดโปรแกรมและเปิดใหม่ใน 5 วินาที...")
                start_completion_timer()  # เรียกฟังก์ชันเริ่มนับถอยหลังและรันใหม่

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

# UI setup
window = tk.Tk()
window.title("Pose Detection")
window.attributes("-fullscreen", True)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

video_label = tk.Label(window)
video_label.pack(fill="both", expand=True)

control_frame = tk.Frame(window)
control_frame.pack(pady=10)

start_button = tk.Button(control_frame, text="เริ่ม", command=start_pose_detection)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(control_frame, text="หยุด", command=stop_pose_detection)
stop_button.grid(row=0, column=1, padx=5)

repeat_label = tk.Label(control_frame, text="จำนวนครั้งที่ต้องทำ")
repeat_label.grid(row=0, column=2, padx=5)

repeat_selector = ttk.Combobox(control_frame, values=[2, 3], state="readonly")
repeat_selector.set(2)
repeat_selector.grid(row=0, column=3, padx=5)
repeat_selector.bind("<<ComboboxSelected>>", lambda e: select_repeats(repeat_selector.get()))

status_label = tk.Label(window, text="", font=("THSarabunNew", 16), justify="left")
status_label.pack(pady=10)

cap = cv2.VideoCapture(0)
window.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), window.destroy()])
window.mainloop()
