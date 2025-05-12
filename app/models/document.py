from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class Document(db.Model):
    __tablename__ = 'documents'

    if environment == 'production':
        __table_args__ = {"schema":SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable = False)
    filename = db.Column(db.String(120), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    amount_due = db.Column(db.String, nullable=True)
    vendor_detected = db.Column(db.String, nullable=True)
    was_useful = db.Column(db.Boolean, default=True)
    corrections = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)