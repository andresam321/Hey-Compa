from app.models import PaymentGuide
import pytesseract
from PIL import Image
import re 
import dateparser

 
def extract_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)

def parse_due_date(text):
    date_patterns = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    for date_str in date_patterns:
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            return parsed_date.date()
    return None

def find_amount(text):
    match = re.search(r'\$[\d,.]+', text)
    return match.group() if match else None

def detect_vendor(text, user_id):
    # Get vendor names from this user’s saved guides
    guides = PaymentGuide.query.filter_by(user_id=user_id).all()
    for guide in guides:
        if guide.vendor_name.lower() in text.lower():
            return guide.vendor_name
    return "Unknown"
