from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class GuideProgress(db.Model):
    __tablename__ = 'guide_progress'

    if environment == 'production':
        __table_args__ = {"schema": SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    payment_guide_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('payment_guides.id')), nullable=False)
    vendor_name = db.Column(db.String, nullable=False)
    current_step = db.Column(db.Integer, default=0)
    is_complete = db.Column(db.Boolean, default=False)
    stuck_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', back_populates='guide_progress', lazy=True)
    payment_guide = db.relationship('PaymentGuide', back_populates='guide_progress')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "payment_guide_id": self.payment_guide_id,
            "vendor_name": self.vendor_name,
            "current_step": self.current_step,
            "is_complete": self.is_complete,
            "stuck_count": self.stuck_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }