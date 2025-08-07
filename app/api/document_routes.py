from flask import Blueprint, request, jsonify
from app.models import Document, db, PaymentGuide, GuideProgress
from flask_login import login_required, current_user
from uuid import uuid4
from werkzeug.utils import secure_filename
from app.forms import DocumentForm
import os
from app.utils.ocr_utils import compute_image_hash
# from app.celery_app import process_document  # ✅ Celery task
from app.tasks.task import process_document
from celery.result import AsyncResult
# from app.celery_app import app as celery_app  # Import the Celery appc
from app.tasks.task import app as celery_app
import json
doc_routes = Blueprint('documents', __name__)

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

    # Compute hash
    image_hash = compute_image_hash(temp_path)
    existing_doc = Document.query.filter_by(user_id=user_id, image_hash=image_hash).first()
    print("existing_doc:", existing_doc.payment_guide_id if existing_doc else None)
#     if existing_doc:
#         guide_progress = GuideProgress.query.filter_by(user_id=user_id, payment_guide_id=existing_doc.payment_guide_id).first()
#         step_texts_raw = existing_doc.payment_guide.step_texts
# # Handle JSON string or direct list
#         step_texts = json.loads(step_texts_raw) if isinstance(step_texts_raw, str) else step_texts_raw or []

#         current_step = guide_progress.current_step if guide_progress else 1
#         current_step_text = (
#             step_texts[current_step - 1] if step_texts and len(step_texts) >= current_step else None
#         )

#         return jsonify({
#             'step_texts': step_texts,
#             'current_step_text': current_step_text,
#             'vendor_detected': existing_doc.vendor_detected,
#             'progress': current_step,
#             'message': 'Exact document match — resuming where you left off' if guide_progress else 'Exact document match — starting at step 1'
#         })


    # Create placeholder doc row
    new_doc = Document(user_id=user_id, image_hash=image_hash)
    db.session.add(new_doc)
    db.session.commit()
    print("New document created with ID:", new_doc.id)
    # Launch background task
    task = process_document.delay(temp_path, user_id, new_doc.id)

    return jsonify({
        'job_id': task.id,
        'message': 'Document is being processed. Use /status/<job_id> to retrieve the result.'
    }), 202


@doc_routes.route('/status/<job_id>', methods=['GET'])
@login_required
def get_processing_status(job_id):
    result = AsyncResult(job_id, app=celery_app) 

    if result.ready():
        if result.successful():
            return jsonify({"status": "done", "result": result.result}), 200
        else:
            return jsonify({"status": "failed", "error": str(result.result)}), 500

    return jsonify({"status": "processing"}), 202
# if same_image_uploaded_before:
#     if guide_progress_exists:
#         return progress + step_texts + resume_msg
#     else:
#         return step_texts + start_over_msg
# else:
#     save_doc()
#     launch_celery_worker()
#     return job_id + processing_msg