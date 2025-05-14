from flask import Blueprint, request, jsonify, json
from app.models import Document, db, PaymentGuide
from flask_login import login_required,current_user
from app.utils.donut_utils import extract_with_donut
import os

from app.utils.ocr_utils import detect_vendor, parse_due_date, find_amount, extract_image_text, parse_account_number, extract_phone_number, extract_phone_number

doc_routes = Blueprint('documents', __name__)

@doc_routes.route('/image', methods=['POST'])
@login_required
def submit_document_from_image():
    user_id = current_user.id
    image = request.files.get('image')  # expects multipart/form-data

    if not user_id or not image:
        return jsonify({'error': 'user_id and image are required'}), 400

    # Save file temporarily
    filename = image.filename
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    image.save(filepath)

    try:
        # 🧠 Try Donut first
        donut_output = extract_with_donut(filepath)
        print(f"📄 Processing file: {filename}")
        print("🍩 Donut Output:", repr(donut_output))

        try:
            parsed = json.loads(donut_output)
        except Exception as e:
            print(f"❌ Donut parsing failed: {e}")
            parsed = {}

        # Extract from Donut if available, fallback to OCR if missing
        extracted_text = parsed.get("extracted_text") or extract_image_text(image)
        vendor = parsed.get("vendor") or detect_vendor(extracted_text, user_id)
        expiration = parsed.get("due_date") or parse_due_date(extracted_text)
        amount = parsed.get("amount_due") or find_amount(extracted_text)
        phone_number = parsed.get("phone_number") or extract_phone_number(extracted_text)
        account_number = parsed.get("account_number") or parse_account_number(extracted_text)

        guide = PaymentGuide.query.filter_by(user_id=user_id, vendor_name=vendor).first()

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

        return jsonify({
            'message': 'Document processed and stored successfully.',
            'vendor_detected': vendor,
            'amount_due': amount,
            'expiration_date': str(expiration) if expiration else None,
            'account_number': account_number,
            'phone_number': phone_number,
            'extracted_text': extracted_text
        }), 201

    except json.JSONDecoder as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500

    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
