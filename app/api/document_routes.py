from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide
from app.utils import detect_vendor, parse_amount, parse_due_date, find_amount, extract_text

doc = Blueprint('Document', __name__)


@doc.route('/document', methods=['POST'])
def submit_document():
    data = request.get_json()
    user_id = data.get('user_id')
    filename = data.get('filename')
    extracted_text = data.get('text')

    if not user_id or not filename or not extracted_text:
        return jsonify({'error': 'Missing required fields'}), 400

    # Extract structured fields
    vendor = detect_vendor(extracted_text, user_id)
    expiration = parse_due_date(extracted_text)
    total_amount = find_amount(extracted_text)
    extract_txt = extract_text(extracted_text)

    # Save document to DB
    doc = Document(
        user_id=user_id,
        filename=filename,
        extracted_text=extracted_text,
        vendor_detected=vendor,
        expiration_date=expiration,
        total_amount=total_amount,
        extract_txt=extract_txt
    )
    db.session.add(doc)
    db.session.commit()

    return jsonify({
        'message': 'Document processed and stored successfully.',
        'vendor_detected': vendor,
        'amount_due': total_amount,
        'expiration_date': str(expiration) if expiration else None
    }), 201