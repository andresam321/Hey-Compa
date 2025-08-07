import os
import time
import threading
from PIL import Image, ImageEnhance, UnidentifiedImageError
import numpy as np
# from paddleocr import PaddleOCR

# Thread-safe OCR instance
ocr_lock = threading.Lock()
# ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

# Ensure the image is fully written to disk before running OCR
# def wait_for_file_write_complete(path, timeout=3):
#     prev_size = -1
#     for _ in range(int(timeout * 10)):  # Check every 0.1s
#         try:
#             current_size = os.path.getsize(path)
#         except FileNotFoundError:
#             time.sleep(0.1)
#             continue
#         if current_size == prev_size:
#             return True
#         prev_size = current_size
#         time.sleep(0.1)
#     return False

# Main OCR runner
def run_paddle_ocr(ocr_instance, image_path, retries=3):
    for attempt in range(retries):
        try:
            print(f"OCR Attempt {attempt+1} on: {image_path}")

            img = Image.open(image_path).convert("RGB")
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3.0)
            img.thumbnail((1200, 1200))
            img_np = np.array(img)

            result = ocr_instance.ocr(img_np, cls=True)
            return result

        except Exception as e:
            print(f"OCR attempt {attempt+1} failed:", e)
            time.sleep(0.5)

    return None