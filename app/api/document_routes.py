from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide
from flask_login import login_required,current_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.forms import DocumentForm
import hashlib
import os
import time
from app.utils.openai_utils import generate_steps_from_text, parse_steps
from app.utils.ocr_utils import detect_vendor, parse_due_date, find_amount, extract_image_text, parse_account_number, extract_phone_number, extract_phone_number, normalize_text

doc_routes = Blueprint('documents', __name__)

#tested
@doc_routes.route('/image/upload', methods=['POST'])
@login_required
def submit_document_from_image():
    form = DocumentForm()
    print("Form data:",form)
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
    # No existing guide — generate fresh steps
            raw_steps = generate_steps_from_text(extracted_text, normalized_vendor)
            steps = parse_steps(raw_steps)

            guide = PaymentGuide(
                user_id=user_id,
                vendor_name=normalized_vendor,
                step_texts=steps,
                step_images=[],
                times_seen = 1,  # Initialize with 1 since this is the first time processing
            )
            db.session.add(guide)
            db.session.commit()

        else:
            # Guide exists — generate new steps from doc
            raw_new_steps = generate_steps_from_text(extracted_text, normalized_vendor)
            new_steps = parse_steps(raw_new_steps)
            existing_steps = guide.step_texts if guide.step_texts else []
            cleaned_existing = [step.lower().strip() for step in existing_steps]

            for step in new_steps:
                clean_step = step.lower().strip()
                if not any(clean_step in existing or existing in clean_step for existing in cleaned_existing):
                    print("Appending new step:", step)
                    existing_steps.append(step)

            guide.step_texts = existing_steps
            guide.times_seen = (guide.times_seen or 0) + 1
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
            'extracted_text': extracted_text,
            'step_texts': guide.step_texts
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to process image: {str(e)}'}), 500