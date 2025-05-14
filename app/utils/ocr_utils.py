from app.models import PaymentGuide
import pytesseract
from thefuzz import fuzz
from PIL import Image
import re 
import dateparser

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


def detect_vendor(text, user_id=None):
    normalized_text = text.lower()

    # 🔍 Fuzzy match to handle OCR garble
    for keyword, vendor in vendor_keywords.items():
        if fuzz.partial_ratio(keyword, normalized_text) >= 80:
            return vendor

    # Optional: fallback to user’s guides
    if user_id:
        guides = PaymentGuide.query.filter_by(user_id=user_id).all()
        for guide in guides:
            if guide.vendor_name.lower() in normalized_text:
                return guide.vendor_name

    return "Unknown"




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



def parse_account_number(text):
    match = re.search(r'\d{5,}-\d{4,}', text)
    return match.group() if match else None

def extract_phone_number(text):
    match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    return match.group() if match else None
