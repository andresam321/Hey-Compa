from app.models import PaymentGuide
from PIL import Image, ImageEnhance, ImageFilter
import re 
import dateparser
from thefuzz import process, fuzz
import numpy as np
from PIL import Image
import re
from app.utils.ocr_helpers import run_paddle_ocr

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
    "san diego gas": "SDG&E",
    "maine natural gas": "Maine Natural Gas",
    "tucson electric power": "Tucson Electric Power",
    "waste management": "Waste Management",
    "city of boise utility billing service": "City of Boise Utility Billing Service",
    "north clinic": "North Clinic",
}


#loads ocr engine once at module level, lang = language 'english
#use_angle_cls=True helps detect rotated text (e.g., slanted/tilted labels).

def extract_image_text(image_path):
    result = run_paddle_ocr(image_path)
    if not result or not result[0]:
        return ""
    lines = []
    for line in result[0]:
        if isinstance(line, list) and len(line) == 2:
            box, text_info = line
            if isinstance(text_info, tuple) and len(text_info) == 2:
                text, _ = text_info
                lines.append(text)
    return "\n".join(lines)

#uses regex to find the due date in the text
#uses dateparser to parse the date string into a date object
def parse_due_date(text):
    date_patterns = [
        r'(due by|due on|date due|due date|effective date|data filed)?[:\s\n]*([A-Za-z]{3,9}\.?[\s\-]?\d{1,2},?\s?\d{4})',
        r'(due by|due on|date due|due date|effective date|data filed)?[:\s\n]*([\d]{1,2}[/-][\d]{1,2}[/-][\d]{2,4})'
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for _, date_str in matches:
            parsed = dateparser.parse(date_str)
            if parsed:
                return parsed.date()
    return None

#uses regex to find the amount in the text
#fallbacks to a different regex if no matches are found
#uses max to find the largest amount in the text
def find_amount(text):
    # Normalize text
    text = text.lower()

    # Step 1: Context-aware match
    due_patterns = [
        r'(amount due[:\s]*)\$[\d,]+\.\d{2}',
        r'(due now[:\s]*)\$[\d,]+\.\d{2}',
        r'(total due[:\s]*)\$[\d,]+\.\d{2}',
        r'(please pay[:\s]*)\$[\d,]+\.\d{2}'
    ]

    for pattern in due_patterns:
        match = re.search(pattern, text)
        if match:
            amount = re.search(r'\$[\d,]+\.\d{2}', match.group())
            if amount:
                return amount.group()

    # Step 2: Fallback — find all dollar amounts
    matches = re.findall(r'\$[\d,]+\.\d{2}', text)
    if not matches:
        matches = re.findall(r'\$\d{3,}', text)

    # Step 3: Return lowest if no context match
    if matches:
        try:
            return min(matches, key=lambda x: float(x.replace('$','').replace(',','')))
        except:
            pass

    return None

#uses fuzzy matching to find the vendor in the text
#checks each line of text with the vendor keywords
#uses thefuzz library to find the best match
def detect_vendor(text, user_id=None):
    normalized_text = text.lower()
    lines = normalized_text.splitlines()

    best_match = ("", 0)

    for line in lines:
        for keyword, vendor in vendor_keywords.items():
            if keyword in line:
                # Exact keyword found in line
                return vendor

            score = fuzz.partial_ratio(keyword, line)
            if score > best_match[1]:
                best_match = (keyword, score)

    # Only accept fuzzy matches above high confidence
    if best_match[1] >= 85:
        return vendor_keywords[best_match[0]]

    # Fallback to user's saved guides
    if user_id:
        guides = PaymentGuide.query.filter_by(user_id=user_id).all()
        for guide in guides:
            if guide.vendor_name.lower() in normalized_text:
                return guide.vendor_name

    return "Unknown"

#uses regex to find the account number in the text
#matches a pattern of 5 or more digits followed by a hyphen and 4 or more digits
def parse_account_number(text):
    match = re.search(r'\d{5,}-\d{4,}', text)
    return match.group() if match else None

#matches a pattern of 3 digits followed by an optional hyphen or space and 3 more digits followed by an optional hyphen or space and 4 digits
def extract_phone_number(text):
    match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group() if match else None

#not tested
def normalize_text(text):
    text = re.sub(r"\$?\d+(\.\d{2})?", "", text)  # remove amounts
    text = re.sub(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "", text)  # remove dates
    text = re.sub(r"\d{6,}", "", text)  # remove long account numbers
    return text.lower().strip()