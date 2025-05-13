from app.models import db, environment, SCHEMA, Document
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from faker import Faker
import random

fake = Faker()

VENDORS = [
    "Verizon", "PG&E", "T-Mobile", "Comcast", "AT&T",
    "Spectrum", "Xfinity", "Chase", "Bank of America", "Wells Fargo"
]

def seed_documents_for_nlp(user_id=1, num_docs=50, guide_map=None):
    documents = []

    for _ in range(num_docs):
        vendor = random.choice(VENDORS)
        amount = f"${random.randint(50, 500)}.00"
        days_ahead = random.randint(5, 45)
        due_date = datetime.utcnow() + timedelta(days=days_ahead)

        extracted_text = f"""
            Thank you for choosing {vendor}. 
            Your total amount due is {amount}. 
            Please pay by {due_date.strftime('%m/%d/%Y')}. 
            Visit {vendor.lower().replace(" ", "")}.com for more information.
            For help call {fake.phone_number()}.
        """
        guide = guide_map.get(vendor) if guide_map else None

        doc = Document(
            user_id=user_id,
            extracted_text=extracted_text.strip(),
            vendor_detected=vendor,
            expiration_date=due_date,
            amount_due=amount,
            phone_number=fake.phone_number(),
            account_number=fake.bothify(text='####-####-####'),
            was_useful=random.choice([True, False]),
            corrections=None,
            payment_guide_id=guide.id if guide else None
        )

        documents.append(doc)

    db.session.add_all(documents)
    db.session.commit()

def undo_documents():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.documents RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM documents"))

    db.session.commit()
