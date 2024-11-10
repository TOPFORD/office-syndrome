import cv2
import mediapipe as mp
from PIL import Image, ImageFont, ImageDraw, ImageTk
import numpy as np
import tkinter as tk
from tkinter import ttk
import pygame
from completion_timer import CompletionTimer
import time

# นำเข้าฟังก์ชันที่ใช้โหลดรูปภาพจากไฟล์แยก
from pose_images_loader import load_all_pose_images, retrieve_pose_image

from posture1 import check_posture1
from posture2L import check_posture2L
from posture2R import check_posture2R
from posture3L import check_posture3L
from posture3R import check_posture3R
from posture4L import check_posture4L
from posture4R import check_posture4R
from posture5L import check_posture5L
from posture5R import check_posture5R
from posture6L import check_posture6L
from posture6R import check_posture6R

# อัปเดตข้อมูลท่าและแขนข้างใน posture_checks
posture_checks = [
    (check_posture1, "ท่าที่ 1", ""),  # ท่าที่ 1 ไม่มีข้อมูลแขนข้าง
    (check_posture2R, "ท่าที่ 2", "ข้างขวา"),
    (check_posture2L, "ท่าที่ 2", "ข้างซ้าย"),
    (check_posture3R, "ท่าที่ 3", "ข้างขวา"),
    (check_posture3L, "ท่าที่ 3", "ข้างซ้าย"),
    (check_posture4R, "ท่าที่ 4", "ข้างขวา"),
    (check_posture4L, "ท่าที่ 4", "ข้างซ้าย"),
    (check_posture5R, "ท่าที่ 5", "ข้างขวา"),
    (check_posture5L, "ท่าที่ 5", "ข้างซ้าย"),
    (check_posture6R, "ท่าที่ 6", "ข้างขวา"),
    (check_posture6L, "ท่าที่ 6", "ข้างซ้าย")
]

# โหลดภาพท่าทางทั้งหมดเมื่อโปรแกรมเริ่มทำงาน
pose_images = load_all_pose_images()

# Initialize MediaPipe and pygame
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Load Thai bold font with larger size
try:
    font_path = "THSarabunNew.ttf"  # ใช้ฟอนต์ตัวหนา
    font = ImageFont.truetype(font_path, 40)  # กำหนดขนาดฟอนต์ให้ใหญ่ขึ้นเป็น 40
except IOError:
    print("ฟอนต์ 'THSarabunNew.ttf' ไม่พบ, ใช้ฟอนต์ Arial แทน")
    font_path = "arial.ttf"
    font = ImageFont.truetype(font_path, 40)

pygame.init()
alert_sound = pygame.mixer.Sound("Audio.MP3")

# Set initial states
start_time = None
current_pose = 1
target_repeats = 1  # จำนวนครั้งที่ต้องทำสำหรับแต่ละท่า
current_repeats = 0
completed_time = None
is_running = False

# สร้างหน้าต่างหลักของ Tkinter
window = tk.Tk()
window.title("Pose Detection")
window.geometry("1280x720")
window.configure(bg="#2e2e2e")

def select_repeats(value):
    global target_repeats
    target_repeats = int(value)

def track_pose(posture_check, results_pose, results_hands, image, current_pose, target_repeats, start_time, current_repeats):
    is_correct_pose = False
    # ตรวจสอบว่าฟังก์ชัน posture_check ต้องการอาร์กิวเมนต์ image หรือไม่
    if current_pose in [10, 11]:  # ท่าที่ต้องใช้การตรวจสอบมือและ image
        is_correct_pose = posture_check(results_pose, results_hands, image)
    else:
        is_correct_pose = posture_check(results_pose)

    if is_correct_pose:
        if start_time is None:
            start_time = time.time()
        elif time.time() - start_time >= 10:  # ทำท่าถูกต้องค้างไว้อย่างน้อย 2 วินาที
            alert_sound.play()
            start_time = None
            current_repeats += 1
            if current_repeats >= target_repeats:  # ตรวจสอบว่าทำครบจำนวนครั้งที่ต้องทำหรือยัง
                return True, start_time, current_repeats
    else:
        start_time = None
    return False, start_time, current_repeats


def start_completion_timer():
    """เรียกใช้ CompletionTimer เมื่อทำท่าครบ"""
    completion_timer = CompletionTimer(countdown_time=5)
    window.destroy()
    completion_timer.start_and_restart()

def start_pose_detection():
    global is_running, start_time, current_repeats, completed_time, current_pose
    is_running = True
    start_time = None
    current_repeats = 0
    completed_time = None
    current_pose = 1  # รีเซ็ตท่าปัจจุบันเมื่อเริ่มใหม่
    update_frame()

def update_frame():
    global start_time, is_running, current_pose, current_repeats, completed_time
    if not is_running:
        return

    success, frame = cap.read()
    if not success:
        return

    frame = cv2.resize(frame, (video_label.winfo_width(), video_label.winfo_height()))
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(image)
    results_hands = hands.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # รับข้อมูลท่าและข้างจาก posture_checks
    posture_check, pose_name, side = posture_checks[current_pose - 1]

    # กำหนดรูปภาพตามท่าและข้าง
    if current_pose == 1:
        pose_image = retrieve_pose_image(pose_images, 1)  # รูปสำหรับท่าที่ 1
    elif current_pose in [2, 3]:  # ท่าที่ 2 R และ L ใช้รูปที่ 2
        pose_image = retrieve_pose_image(pose_images, 2)
    elif current_pose in [4, 5]:  # ท่าที่ 3 R และ L ใช้รูปที่ 3
        pose_image = retrieve_pose_image(pose_images, 3)
    elif current_pose in [6, 7]:  # ท่าที่ 4 R และ L ใช้รูปที่ 4
        pose_image = retrieve_pose_image(pose_images, 4)
    elif current_pose in [8, 9]:  # ท่าที่ 5 R และ L ใช้รูปที่ 5
        pose_image = retrieve_pose_image(pose_images, 5)
    elif current_pose in [10, 11]:  # ท่าที่ 6 R และ L ใช้รูปที่ 6
        pose_image = retrieve_pose_image(pose_images, 6)
    else:
        pose_image = None  # กรณีที่ไม่มีรูปภาพ

    if pose_image:
        resized_pose_image = pose_image.resize((300, 200))
        image_pil = Image.fromarray(image)
        image_pil.paste(resized_pose_image, (image_pil.width - 310, 10))
        image = np.array(image_pil)

    if results_pose.pose_landmarks:
        mp_drawing.draw_landmarks(image, results_pose.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        pose_complete, start_time, current_repeats = track_pose(
            posture_check, results_pose, results_hands, image, current_pose, target_repeats, start_time, current_repeats
        )

        if pose_complete:
            status_label.config(text=f"{pose_name} {side} ผ่านแล้ว! ทำครบ {target_repeats} ครั้ง")
            current_pose += 1
            current_repeats = 0
            if current_pose > len(posture_checks):
                status_label.config(text="ทำท่าครบทุกท่าแล้ว! ปิดโปรแกรมและเปิดใหม่ใน 5 วินาที...")
                start_completion_timer()

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # เพิ่มข้อความบอกท่าที่กำลังทำและแสดงตรงกลางด้านบน
    text = f"{pose_name} {side} (จำนวนครั้งที่ต้องทำ: {target_repeats})"
    # คำนวณขนาดของข้อความด้วย textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x = (pil_image.width - text_width) // 2  # คำนวณตำแหน่งตรงกลางแนวนอน
    y = 20  # กำหนดตำแหน่ง y ให้ข้อความอยู่ใกล้ด้านบน
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # วาดเครื่องหมายถูกหรือผิดตามผลการตรวจสอบท่าทาง
    if start_time is not None:
        draw.rectangle([(20, 20), (100, 100)], outline="green", width=6)  # กรอบสีเขียว
        draw.line([(30, 70), (55, 90), (90, 40)], fill="green", width=6)  # รูปเครื่องหมายถูก
    else:
        draw.rectangle([(20, 20), (100, 100)], outline="red", width=6)  # กรอบสีแดง
        draw.line([(30, 30), (90, 90)], fill="red", width=6)  # เครื่องหมายผิด (เส้นแรก)
        draw.line([(30, 90), (90, 30)], fill="red", width=6)  # เครื่องหมายผิด (เส้นที่สอง)

    image = np.array(pil_image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imgtk = ImageTk.PhotoImage(image=Image.fromarray(image))
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)
    window.after(10, update_frame)


# UI setup
video_label = tk.Label(window)
video_label.pack(fill="both", expand=True)

control_frame = tk.Frame(window, bg="#4a4a4a")
control_frame.pack(pady=10)

start_button = tk.Button(control_frame, text="เริ่ม", command=start_pose_detection, bg="#6ab04c", fg="white", font=("THSarabunNew", 14))
start_button.grid(row=0, column=0, padx=5)

repeat_label = tk.Label(control_frame, text="จำนวนครั้งที่ต้องทำ", bg="#4a4a4a", fg="white", font=("THSarabunNew", 14))
repeat_label.grid(row=0, column=1, padx=5)

repeat_selector = ttk.Combobox(control_frame, values=list(range(1, 11)), state="readonly")
repeat_selector.set(1)
repeat_selector.grid(row=0, column=2, padx=5)
repeat_selector.bind("<<ComboboxSelected>>", lambda e: select_repeats(repeat_selector.get()))

status_label = tk.Label(window, text="", font=("THSarabunNew", 16), justify="left", bg="#2e2e2e", fg="white")
status_label.pack(pady=10)

cap = cv2.VideoCapture(0)
window.protocol("WM_DELETE_WINDOW", lambda: [cap.release(), window.destroy()])
window.mainloop()
