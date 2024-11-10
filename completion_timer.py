import time
import subprocess
import sys

class CompletionTimer:
    def __init__(self, countdown_time=5):
        self.countdown_time = countdown_time  # เวลาในการนับถอยหลัง (5 วินาที)

    def start_and_restart(self):
        """เริ่มนับเวลาและเปิด main.py ใหม่เมื่อครบเวลา"""
        print(f"เริ่มนับถอยหลัง {self.countdown_time} วินาที...")
        time.sleep(self.countdown_time)  # รอให้เวลาครบ 5 วินาที
        print("ครบเวลาแล้ว เปิดโปรแกรม main.py ใหม่")
        
        # รัน main.py ใหม่
        python = sys.executable
        subprocess.Popen([python, "main.py"])  # รัน main.py ใหม่
