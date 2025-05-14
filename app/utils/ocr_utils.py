from app.models import PaymentGuide
import pytesseract
from PIL import Image
import re 
import dateparser

 
def extract_image_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def parse_due_date(text):
    matches = re.findall(r'(Due by|Due on|Date Due|Due Date)?\s*(\w{3,9} \d{1,2},? \d{4})', text, re.IGNORECASE)
    for _, date_str in matches:
        parsed = dateparser.parse(date_str)
        if parsed:
            return parsed.date()
    return None


def find_amount(text):
    matches = re.findall(r'\$[\d,]+\.\d{2}', text)
    if matches:
        # Pick the largest one — likely the total
        return max(matches, key=lambda x: float(x.replace('$','').replace(',','')))
    return None


def detect_vendor(text, user_id):
    # Get vendor names from this user’s saved guides
    guides = PaymentGuide.query.filter_by(user_id=user_id).all()
    for guide in guides:
        if guide.vendor_name.lower() in text.lower():
            return guide.vendor_name
    return "Unknown"

def parse_account_number(text):
    match = re.search(r'\d{5,}-\d{4,}', text)
    return match.group() if match else None

def extract_phone_number(text):
    match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group() if match else None
