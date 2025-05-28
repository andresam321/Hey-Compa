from .db import db, environment, SCHEMA, add_prefix_for_prod
from datetime import datetime

class PaymentGuide(db.Model):
    __tablename__ = 'payment_guides'

    __table_args__ = (
        db.UniqueConstraint('user_id', 'vendor_name', name='unique_user_vendor'),
        {"schema": SCHEMA} if environment == "production" else {}
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable = False)
    vendor_name = db.Column(db.String(120), nullable=False)
    step_texts = db.Column(db.JSON, nullable=False)  
    step_images = db.Column(db.JSON, nullable=True)
    times_seen = db.Column(db.Integer, nullable=True, default=1)  
    # ai_step_texts = db.Column(db.JSON, nullable=True)  # Optional AI-generated steps
    # ai_step_images = db.Column(db.JSON, nullable=True)  # Optional AI-generated images 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    user = db.relationship('User', back_populates='payment_guides', lazy=True)
    documents = db.relationship('Document', back_populates='payment_guide', lazy=True)
    guide_progress = db.relationship('GuideProgress', back_populates='payment_guide', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "vendor_name":self.vendor_name,
            "step_texts":self.step_texts,
            "step_images":self.step_images,
            "times_seen": self.times_seen,
            "updated_at": self.updated_at,
            "created_at": self.created_at

        }