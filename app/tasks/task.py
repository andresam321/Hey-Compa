from celery import Celery
from paddleocr import PaddleOCR
from app.utils.ocr_helpers import run_paddle_ocr
from app.utils.ocr_utils import (
    detect_vendor,
    find_amount,
    parse_due_date,
    parse_account_number,
    extract_phone_number,
    extract_image_text
   
)
from app.utils.openai_utils import generate_steps_from_text, parse_steps
from app.models import db, Document, PaymentGuide
import os

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)

@app.task
def process_document(image_path, user_id, doc_id):
        try:
            # OCR + Extraction
            extracted_text = extract_image_text(image_path, ocr)
            vendor = detect_vendor(extracted_text, user_id)
            expiration = parse_due_date(extracted_text)
            amount = find_amount(extracted_text)
            phone_number = extract_phone_number(extracted_text)
            account_number = parse_account_number(extracted_text)
            normalized_vendor = vendor.strip().lower()

            # Guide handling
            guide = PaymentGuide.query.filter_by(user_id=user_id, vendor_name=normalized_vendor).first()

            if not guide:
                raw_steps = generate_steps_from_text(extracted_text, normalized_vendor)
                print("RAW STEPS:", raw_steps)
                steps = parse_steps(raw_steps)
                print("PARSED STEPS:", steps)
                guide = PaymentGuide(
                    user_id=user_id,
                    vendor_name=normalized_vendor,
                    step_texts=steps,
                    step_images=[],
                    times_seen=1
                )
                db.session.add(guide)
                db.session.commit()
            else:
                raw_new_steps = generate_steps_from_text(extracted_text, normalized_vendor)
                new_steps = parse_steps(raw_new_steps)
                existing_steps = guide.step_texts or []
                cleaned_existing = [s.lower().strip() for s in existing_steps]

                for step in new_steps:
                    clean_step = step.lower().strip()
                    if not any(clean_step in exist or exist in clean_step for exist in cleaned_existing):
                        existing_steps.append(step)

                guide.step_texts = existing_steps
                guide.times_seen = (guide.times_seen or 0) + 1
                db.session.commit()

            # Update document
            doc = Document.query.get(doc_id)
            doc.extracted_text = extracted_text
            doc.vendor_detected = vendor
            doc.expiration_date = expiration
            doc.amount_due = amount
            doc.phone_number = phone_number
            doc.account_number = account_number
            doc.payment_guide_id = guide.id
            db.session.add(doc)
            db.session.commit()

            return {
                'message': 'Document processed and saved.',
                'vendor_detected': vendor,
                'step_texts': guide.step_texts,
                'doc_id': doc.id
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
