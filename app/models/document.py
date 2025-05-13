from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'

    if environment == 'production':
        __table_args__ = {"schema":SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable = False)
    payment_guide_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('payment_guides.id')), nullable=True)
    extracted_text = db.Column(db.Text, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.String(100), nullable=True)
    amount_due = db.Column(db.String, nullable=True)
    vendor_detected = db.Column(db.String, nullable=True)
    was_useful = db.Column(db.Boolean, default=True)
    corrections = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='documents', lazy=True)

    payment_guide = db.relationship('PaymentGuide', backref='documents', lazy=True)


    def to_dict(self):
        return{
            "id":self.id,
            "user_id":self.user_id,
            "payment_guide_id":self.payment_guide_id,
            "extracted_text":self.extracted_text,
            "expiration_date":self.expiration_date,
            "amount_due":self.amount_due,
            "vendor_detected":self.vendor_detected,
            "was_useful":self.was_useful,
            "corrections":self.corrections,
            "phone_number":self.phone_number,
            "account_number":self.account_number,
            "created_at":self.created_at
        }