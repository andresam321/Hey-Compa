from flask import Blueprint, request, jsonify
from app.models import db, PaymentGuide, Document

payment_guide_routes = Blueprint('payment_guide', __name__)

@payment_guide_routes.route('/payment-guide/<vendor>', methods=['GET'])
def get_or_generate_guide(vendor):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    guide = PaymentGuide.query.filter_by(vendor_name=vendor, user_id=user_id).first()
    if guide:
        return jsonify({
            'vendor_name': guide.vendor_name,
            'step_texts': guide.step_texts,
            'step_images': guide.step_images,
            'message': 'Guide retrieved successfully.'
        }), 200
    
    document = Document.query.filter_by(user_id=user_id, vendor_detected=vendor).order_by(Document.created_at.desc()).first()

    if not document:
        return jsonify({
            'vendor_name': vendor,
            'payment_guide': None,
            'message': 'No document found for this vendor.'
        }), 404
    # Generate a new guide based on the document
    rough_guide_steps = [
       f"Search for '{vendor}' website",
        "Log in to your account",
        "Navigate to the payment section",
        "Enter the amount due",
        "Select payment method",
        "Confirm payment"
    ]
    return jsonify({
        'vendor': vendor,
        'step_texts': rought_guide_steps,
        'message': 'No guide existed, draft steps generated. Please review or confirm.'
    }), 200