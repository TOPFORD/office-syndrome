from PIL import Image

def load_all_pose_images():
    """โหลดรูปภาพที่ใช้สำหรับท่าทางแต่ละท่า"""
    pose_images = []
    for i in range(1, 7):
        try:
            pose_image = Image.open(f"pose{i}.png")
            pose_images.append(pose_image)
        except Exception as e:
            print(f"Error loading image for pose {i}: {e}")
    return pose_images

def retrieve_pose_image(pose_images, pose_index):
    """คืนค่า Image ของท่าที่ถูกต้องตาม pose_index"""
    try:
        return pose_images[pose_index - 1]  # คืนค่าภาพที่สัมพันธ์กับท่าที่กำลังทำ
    except IndexError as e:
        print("Error getting image:", e)
    return None
