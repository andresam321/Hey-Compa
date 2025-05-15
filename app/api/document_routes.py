from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide
from flask_login import login_required,current_user
from uuid import uuid4
from werkzeug.utils import secure_filename
import os
from app.utils.ocr_utils import detect_vendor, parse_due_date, find_amount, extract_image_text, parse_account_number, extract_phone_number, extract_phone_number

doc_routes = Blueprint('documents', __name__)

#tested
@doc_routes.route('/image', methods=['POST'])
@login_required
def submit_document_from_image():
    user_id = current_user.id
    image = request.files.get('image')  # expects multipart/form-data

    if not user_id or not image:
        return jsonify({'error': 'user_id and image are required'}), 400

    # Save image to temp path before processing
    original_filename = secure_filename(image.filename)  # preserves extension
    ext = os.path.splitext(original_filename)[1]  # e.g., ".jpg" or ".png"
    filename = f"{uuid4()}{ext}"
    os.makedirs("uploads", exist_ok=True)
    temp_path = os.path.join("app/uploads", filename)
    image.save(temp_path)
    print("Saved image to:", temp_path)
    
    if not ext.lower() in [".png", ".jpg", ".jpeg", ".webp"]:
        return jsonify({"error": "Unsupported image format"}), 400

    try:
        # Step 1: Run OCR
        extracted_text = extract_image_text(temp_path)
        # print("🔍 Extracted Text:", extracted_text)

        # Step 2: Run parsing logic
        vendor = detect_vendor(extracted_text, user_id)
        expiration = parse_due_date(extracted_text)
        amount = find_amount(extracted_text)
        phone_number = extract_phone_number(extracted_text)
        account_number = parse_account_number(extracted_text)
        # Optional: Save phone number and account number to the document 

        guide = PaymentGuide.query.filter_by(user_id=user_id, vendor_name=vendor).first()
        # Step 3: Save to DB
        doc = Document(
            user_id=user_id,
            extracted_text=extracted_text,
            vendor_detected=vendor,
            expiration_date=expiration,
            amount_due=amount,
            phone_number=phone_number,
            account_number=account_number,
            payment_guide_id=guide.id if guide else None
        )
        db.session.add(doc)
        db.session.commit()

        # Step 4: Return response
        return jsonify({
            'message': 'Document processed and stored successfully.',
            'vendor_detected': vendor,
            'amount_due': amount,
            'expiration_date': str(expiration) if expiration else None,
            'account_number': account_number,
            'phone_number': phone_number,
            'extracted_text': extracted_text
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500
      