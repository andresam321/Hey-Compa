from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide
from flask_login import login_required,current_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.forms import DocumentForm
import os
import time
from app.utils.ocr_utils import detect_vendor, parse_due_date, find_amount, extract_image_text, parse_account_number, extract_phone_number, extract_phone_number

doc_routes = Blueprint('documents', __name__)

#tested
@doc_routes.route('/image/upload', methods=['POST'])
@login_required
def submit_document_from_image():
    form = DocumentForm()

    form["csrf_token"].data = request.cookies.get("csrf_token")

    if not form.validate_on_submit():
        return jsonify({'errors': form.errors}), 400

    image = form.image.data
    user_id = current_user.id

    original_filename = secure_filename(image.filename)
    ext = os.path.splitext(original_filename)[1]
    filename = f"{uuid4()}{ext}"
    os.makedirs("app/uploads", exist_ok=True)
    temp_path = os.path.join("app/uploads", filename)
    image.save(temp_path)

    try:
        # OCR and extraction
        extracted_text = extract_image_text(temp_path)
        vendor = detect_vendor(extracted_text, user_id)
        expiration = parse_due_date(extracted_text)
        amount = find_amount(extracted_text)
        phone_number = extract_phone_number(extracted_text)
        account_number = parse_account_number(extracted_text)

        normalized_vendor = vendor.strip().lower()
        guide = PaymentGuide.query.filter_by(user_id=user_id, vendor_name=normalized_vendor).first()

        if not guide:
            steps = [
                f"Search for '{vendor}' website",
                "Log in to your account",
                "Navigate to the payment section",
                "Enter the amount due",
                "Select payment method",
                "Confirm payment"
            ]
            guide = PaymentGuide(
                user_id=user_id,
                vendor_name=normalized_vendor,
                step_texts=steps,
                step_images=[]
            )
            db.session.add(guide)
            db.session.commit()

        doc = Document(
            user_id=user_id,
            extracted_text=extracted_text,
            vendor_detected=vendor,
            expiration_date=expiration,
            amount_due=amount,
            phone_number=phone_number,
            account_number=account_number,
            payment_guide_id=guide.id
        )
        db.session.add(doc)
        db.session.commit()

        return jsonify({
            'id': doc.id,
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