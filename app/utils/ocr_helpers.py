# app/utils/ocr_helpers.py
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageEnhance
import threading
import time

# Thread lock to allow only one access at a time
ocr_lock = threading.Lock()

# Initialize OCR once
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

def run_paddle_ocr(image_path, retries=3):
    # Attempt to run OCR up to 'retries' times in case of failure
    for attempt in range(retries):
        try:
            # Open the image and convert it to RGB format
            img = Image.open(image_path).convert("RGB")
            
            # Enhance the contrast of the image to help OCR accuracy
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(3.0)

            # Resize the image to make smaller text more detectable
            img = img.resize((img.width * 2, img.height * 2))

            # Convert the PIL image to a NumPy array for PaddleOCR
            img_np = np.array(img)

            # Use a thread lock to ensure only one OCR process runs at a time
            with ocr_lock:
                # Perform OCR on the processed image
                result = ocr.ocr(img_np, cls=True)

            # If successful, return the OCR result
            return result

        except Exception as e:
            # If OCR fails, print the attempt number and the error
            print(f"Attempt {attempt+1} failed:", e)

            # Wait briefly before retrying
            time.sleep(0.5)

    # If all attempts fail, return None
    return None

