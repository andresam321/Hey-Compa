from app.models import db, environment, SCHEMA, PaymentGuide
from sqlalchemy.sql import text
from datetime import datetime

VENDORS = [
    "Verizon", "PG&E", "T-Mobile", "Comcast", "AT&T",
    "Spectrum", "Xfinity", "Chase", "Bank of America", "Wells Fargo"
]

def seed_payment_guides_for_vendors(user_id=1):
    guides = []

    for vendor in VENDORS:
        guide = PaymentGuide(
            user_id=user_id,
            vendor_name=vendor,
            step_texts=[
                f"Go to {vendor.lower().replace(' ', '')}.com",
                "Log in to your account",
                "Navigate to the billing section",
                "Enter your payment information",
                "Click Submit"
            ],
            step_images=None,
            created_at=datetime.utcnow()
        )
        guides.append(guide)

    db.session.add_all(guides)
    db.session.commit()

    # Return a dictionary like {'Verizon': <PaymentGuide obj>}
    return {guide.vendor_name: guide for guide in guides}


def undo_payment_guides():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.payment_guides RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM payment_guides"))

    db.session.commit()
