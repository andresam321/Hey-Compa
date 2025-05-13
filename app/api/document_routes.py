from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide
from app.utils import detect_vendor, parse_due_date, find_amount, extract_image_text, parse_account_number, extract_phone_number, extract_phone_number

doc_routes = Blueprint('Document', __name__)


@doc_routes.route('/document/image', methods=['POST'])
def submit_document_from_image():
    user_id = request.form.get('user_id')
    image = request.files.get('image')  # expects multipart/form-data

    if not user_id or not image:
        return jsonify({'error': 'user_id and image are required'}), 400

    try:
        # Step 1: Run OCR
        extracted_text = extract_image_text(image)

        # Step 2: Run parsing logic
        vendor = detect_vendor(extracted_text, user_id)
        expiration = parse_due_date(extracted_text)
        amount = find_amount(extracted_text)
        phone_number = extract_phone_number(extracted_text)
        account_number = parse_account_number(extracted_text)
        # Optional: Save phone number and account number to the document 

        # Step 3: Save to DB
        doc = Document(
            user_id=user_id,
            extracted_text=extracted_text,
            vendor_detected=vendor,
            expiration_date=expiration,
            amount_due=amount,
            phone_number=phone_number,
            account_number=account_number,
        )
        db.session.add(doc)
        db.session.commit()

        # Step 4: Return response
        return jsonify({
            'message': 'Document processed and stored successfully.',
            'vendor_detected': vendor,
            'amount_due': amount,
            'expiration_date': str(expiration) if expiration else None,
            'extracted_text': extracted_text
        }), 201

    except Exception as e:
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500