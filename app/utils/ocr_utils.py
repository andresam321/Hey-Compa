from app.models import PaymentGuide
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re 
import dateparser
from thefuzz import process, fuzz
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
# ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=True)

vendor_keywords = {
    "pg&e": "PG&E",
    "pacific gas and electric": "PG&E",
    "verizon": "Verizon",
    "at&t": "AT&T",
    "att": "AT&T",
    "comcast": "Comcast",
    "xfinity": "Comcast",
    "spectrum": "Spectrum",
    "charter": "Spectrum",
    "t-mobile": "T-Mobile",
    "tmobile": "T-Mobile",
    "centurylink": "CenturyLink",
    "lumen": "CenturyLink",
    "centerpoint": "CenterPoint Energy",
    "centerpoint energy": "CenterPoint Energy",
    "socalgas": "SoCalGas",
    "southern california gas": "SoCalGas",
    "ladwp": "LADWP",
    "los angeles department of water and power": "LADWP",
    "con edison": "Con Edison",
    "coned": "Con Edison",
    "national grid": "National Grid",
    "duke energy": "Duke Energy",
    "georgia power": "Georgia Power",
    "pepco": "Pepco",
    "comed": "ComEd",
    "dominion": "Dominion Energy",
    "fpl": "Florida Power & Light",
    "florida power": "Florida Power & Light",
    "smud": "SMUD",
    "bge": "BGE",
    "pge": "PG&E",
    "nyseg": "NYSEG",
    "sdge": "SDG&E",
    "san diego gas": "SDG&E"
}

# ocr = PaddleOCR(use_angle_cls=True, lang='en')
# image_path = "uploads/2e"  # Use actual path here

# img = Image.open(image_path).convert("RGB")
# img_np = np.array(img)
# result = ocr.ocr(img_np, cls=True)

# print("📸 OCR Result:", result)

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
  # Load once at module level

def extract_image_text(image_path):
    img = Image.open(image_path).convert("RGB")

    # Enhance image to improve OCR accuracy
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(3.0)
    img = img.resize((img.width * 2, img.height * 2))

    img_np = np.array(img)
    result = ocr.ocr(img_np, cls=True)
    print("📸 RAW OCR RESULT:", result)

    if not result or not result[0]:
        return ""

    lines = []
    for line in result[0]:
        if line:
            for word_info in line:
                text = word_info[1][0]
                lines.append(text)

    return "\n".join(lines)


def parse_due_date(text):
    matches = re.findall(
        r'(Due by|Due on|Date Due|Due Date|Effective Date|Data Filed)?[:\s]*([A-Za-z]{3,9}\.? \d{1,2},? \d{4})',
        text,
        re.IGNORECASE
    )
    for _, date_str in matches:
        parsed = dateparser.parse(date_str)
        if parsed:
            return parsed.date()
    return None

def find_amount(text):
    matches = re.findall(r'\$[\d,]+\.\d{2}', text)
    if not matches:
        # Try fallback (e.g., $9422)
        matches = re.findall(r'\$\d{3,}', text)
    if matches:
        try:
            return max(matches, key=lambda x: float(x.replace('$','').replace(',','')))
        except:
            pass
    return None

def detect_vendor(text, user_id=None):
    normalized_text = text.lower()
    lines = normalized_text.splitlines()

    best_match = ("", 0)

    for line in lines:
        for keyword, vendor in vendor_keywords.items():
            if keyword in line:
                # ✅ Exact keyword found in line
                return vendor

            score = fuzz.partial_ratio(keyword, line)
            if score > best_match[1]:
                best_match = (keyword, score)

    # 🎯 Only accept fuzzy matches above high confidence
    if best_match[1] >= 85:
        return vendor_keywords[best_match[0]]

    # 🔁 Fallback to user's saved guides
    if user_id:
        guides = PaymentGuide.query.filter_by(user_id=user_id).all()
        for guide in guides:
            if guide.vendor_name.lower() in normalized_text:
                return guide.vendor_name

    return "Unknown"

def parse_account_number(text):
    match = re.search(r'\d{5,}-\d{4,}', text)
    return match.group() if match else None

def extract_phone_number(text):
    match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group() if match else None
