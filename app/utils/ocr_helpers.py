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
def wait_for_file_write_complete(path, timeout=3):
    prev_size = -1
    for _ in range(int(timeout * 10)):  # Check every 0.1s
        try:
            current_size = os.path.getsize(path)
        except FileNotFoundError:
            time.sleep(0.1)
            continue
        if current_size == prev_size:
            return True
        prev_size = current_size
        time.sleep(0.1)
    return False

# Main OCR runner
def run_paddle_ocr(image_path, retries=3):
    from paddleocr import PaddleOCR  # moved inside
    ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    if not wait_for_file_write_complete(image_path):
        print(f"File write timeout: {image_path}")
        return None

    for attempt in range(retries):
        try:
            print(f"OCR Attempt {attempt+1} on: {image_path}")

            # Load and process image
            try:
                img = Image.open(image_path).convert("RGB")
            except UnidentifiedImageError:
                print("Image could not be opened (possibly corrupted):", image_path)
                return None

            # Save original image for debugging
            # img.save("debug_original.jpg")

            # Enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3.0)

            # Resize for better OCR
            img = img.resize((img.width * 2, img.height * 2))

            # Convert to numpy array
            img_np = np.array(img)
            print("Image shape:", img_np.shape, "dtype:", img_np.dtype)

            # Run OCR inside thread lock
            with ocr_lock:
                result = ocr.ocr(img_np, cls=True)

            # Print and return if successful
            print("OCR Result:", result)
            return result

        except Exception as e:
            print(f"OCR attempt {attempt+1} failed:", e)
            time.sleep(0.5)

    return None
