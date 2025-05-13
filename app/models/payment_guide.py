from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class PaymentGuide(db.Model):
    __tablename__ = 'payment_guides'

    if environment == "production":
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable = False)
    vendor_name = db.Column(db.String(120), nullable=False)
    step_texts = db.Column(db.JSON, nullable=False)  # e.g. ["Go to site", "Click Pay"]
    step_images = db.Column(db.JSON, nullable=True)  # Optional screenshots
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='payment_guides', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "vendor_name":self.vendor_name,
            "step_texts":self.step_texts,
            "step_images":self.step_images

        }