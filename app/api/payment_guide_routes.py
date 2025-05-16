from flask import Blueprint, request, jsonify
from app.models import db, PaymentGuide, Document
from flask_login import login_required, current_user

payment_guide_routes = Blueprint('payment_guide', __name__)

@payment_guide_routes.route('/<vendor>', methods=['GET'])
@login_required
def get_or_generate_guide(vendor):

    user_id = current_user.id
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    
    normalized_vendor = vendor.strip().lower()

    guide = PaymentGuide.query.filter_by(vendor_name=normalized_vendor, user_id=user_id).first()
    if guide:
        return jsonify({
            'vendor_name': guide.vendor_name,
            'step_texts': guide.step_texts,
            'step_images': guide.step_images,
            'message': 'Guide retrieved successfully.'
        }), 200
    
    document = Document.query.filter_by(user_id=user_id,vendor_detected=normalized_vendor).order_by(Document.created_at.desc()).first()
    document = Document.query.filter_by(user_id=user_id, vendor_detected=vendor).order_by(Document.created_at.desc()).first()

    if not document:
        return jsonify({
            'vendor_name': vendor,
            'payment_guide': None,
            'message': 'No document found for this vendor. Please add a new document to create a guide.'
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
        'step_texts': rough_guide_steps,
        'message': 'No guide existed, draft steps generated. Please review or confirm.'
    }), 200

# @payment_guide_routes.route('/payment-guide', methods=['POST'])
# @login_required
# def create_payment_guide():
#     data = request.get_json()
#     user_id = current_user.id
#     vendor_name = data.get('vendor_name')
#     step_texts = data.get('step_texts')
#     step_images = data.get('step_images', [])

#     if not user_id or not vendor_name or not step_texts:
#         return jsonify({'error': 'user_id, vendor_name, and step_texts are required'}), 400

#     # Prevent duplicate guides
#     existing_guide = PaymentGuide.query.filter_by(user_id=user_id, vendor_name=vendor_name).first()
#     if existing_guide:
#         return jsonify({'error': 'Guide already exists for this vendor and user'}), 409

#     # Create and save new guide
#     new_guide = PaymentGuide(
#         user_id=user_id,
#         vendor_name = vendor_name.strip().lower(),
#         step_texts=step_texts,
#         step_images=step_images
#     )
#     db.session.add(new_guide)
#     db.session.commit()

#     return jsonify({
#         'message': 'Payment guide created successfully.',
#         'guide': new_guide.to_dict()
#     }), 201
