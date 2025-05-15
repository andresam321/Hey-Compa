from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)

# ✅ Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)


# ✅ Replace this with an image you already saved (like the Verizon or CenterPoint one)
image_path = "uploads/test_receipt.jpg"  # <-- change this to your real image path

# ✅ Load and convert image
img = Image.open(image_path).convert("RGB")
img_np = np.array(img)

# ✅ Run OCR
result = ocr.ocr(img_np, cls=True)

# ✅ Print result
print("\n📸 OCR Result:")
if result and result[0]:
    for line in result[0]:
        if line:
            for word_info in line:
                print("📝", word_info[1][0])
else:
    print("❌ No text detected.")
