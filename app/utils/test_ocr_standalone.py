from paddleocr import PaddleOCR
from PIL import Image, ImageEnhance
import numpy as np
import os
import cv2
# print("Current directory:", os.getcwd())



ocr = PaddleOCR(use_angle_cls=True, lang='en')

image_path = "app/uploads/test_receipt.jpg"  
img = Image.open(image_path).convert("RGB")
print("line14", np.array(img).shape)

# Log size and format
print(f" Image size: {img.size}, format: {img.format}")

# Optional: Boost contrast
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(2)

# Optional: Resize up
img = img.resize((img.width * 2, img.height * 2))

# Convert to numpy
img_np = np.array(img)
result = ocr.ocr(image_path, cls=True)
# Run OCR
result = ocr.ocr(img_np, cls=True)

print("\n OCR Result:")
if result and result[0]:
    for line in result[0]:
        if len(line) == 2 and isinstance(line[1], tuple):
            text, confidence = line[1]
            print(f"📝 {text} (confidence: {confidence:.2f})")
        else:
            print("⚠️ Skipped malformed entry:", line)