from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import GuideProgress, PaymentGuide, db
import os
from datetime import datetime



guide_progress_routes = Blueprint('guide_progress', __name__)

# tested
@guide_progress_routes.route('/start/<vendor>', methods=['GET'])
@login_required
def start_guide(vendor):
    user_id = current_user.id
    print("Current user ID:", user_id)

    # normalized_vendor = vendor.strip().lower()

    # Check if guide progress already exists
    # existing_progress = GuideProgress.query.filter_by(user_id=user_id, vendor_name=normalized_vendor).first()
    # if existing_progress:
    #     return jsonify({"error": "Guide already exists"}), 400

    # # Fetch the payment guide for the user
    # print(f"[DEBUG] Looking for guide: user_id={user_id}, vendor_name={repr(vendor)}")


    # incomplete = GuideProgress.query.filter(GuideProgress.vendor_name, is_complete = False).order_by(GuideProgress.created_at.desc()).first()
    # if incomplete and (datetime.utcnow() - incomplete.created_at).total_seconds() < 7200:
    #     return resume_session_response(incomplete)
    
    guide = PaymentGuide.query.filter(PaymentGuide.user_id == current_user.id,PaymentGuide.vendor_name.ilike(vendor.strip())).first()
    if not guide:
        print("❌ Payment guide not found")
        return jsonify({"error": "Payment guide not found for this vendor"}), 404
    
    

    # Create new progress with valid payment_guide_id
    new_guide_progress = GuideProgress(
        user_id=user_id,
        vendor_name=vendor,
        payment_guide_id=guide.id,
        current_step=0,
        is_complete=False,
        stuck_count=0
    )

    db.session.add(new_guide_progress)
    db.session.commit()

    return jsonify(new_guide_progress.to_dict()), 201

#tested
@guide_progress_routes.route('/next/<vendor>', methods=['POST'])
@login_required
def next_step(vendor):

    """
    Move to the next step in the guide for the given vendor.
    """
    user_id = current_user.id
    # normalized_vendor = vendor.strip().lower()
    
    guide = PaymentGuide.query.filter(PaymentGuide.user_id == current_user.id, PaymentGuide.vendor_name.ilike(vendor.strip())).first()
    guide_progress = GuideProgress.query.filter_by(user_id=user_id, vendor_name=vendor).first()
    if guide_progress.is_complete:
        guide_progress.current_step = 0
        guide_progress.is_complete = False
        guide_progress.stuck_count = 0
        db.session.commit()
        
        return jsonify({
            "message": "Guide was complete. Starting over from Step 1.",
            "progress": guide_progress.to_dict(),
            "current_instruction": guide.step_texts[0] if guide.step_texts else "No step found"
        }), 200       

    if not guide_progress or not guide:
        return jsonify({"error": "Guide or progress not found"}), 404

    # Increment the current step
    guide_progress.current_step += 1

    # Check if the guide is complete
   
    if guide and guide_progress.current_step >= len(guide.step_texts):
        guide_progress.is_complete = True

    db.session.commit()
    step_index = guide_progress.current_step

# Handle out-of-bounds safety
    step_texts = guide.step_texts or []
    current_instruction = (step_texts[step_index] if 0 <= step_index < len(step_texts) else "All steps completed")

    return jsonify({
    "progress": guide_progress.to_dict(),
    "current_instruction": current_instruction,
    "total_steps": len(step_texts),
    "is_complete": guide_progress.is_complete
}), 200

#tested
@guide_progress_routes.route('/repeat/<vendor>', methods=['POST'])
@login_required
def repeat_step(vendor):
    user_id = current_user.id
    vendor = vendor.strip()

    # Fetch guide and progress
    guide = PaymentGuide.query.filter(PaymentGuide.user_id == current_user.id, PaymentGuide.vendor_name.ilike(vendor.strip())).first()
    progress = GuideProgress.query.filter_by(user_id=user_id, vendor_name=vendor).first()

    if progress.current_step >= len(guide.step_texts):
        progress.current_step = len(guide.step_texts) - 1  # Safety check, and goes to the last step
        progress.is_complete = True

    if not guide or not progress:
        return jsonify({"error": "Guide or progress not found"}), 404
    
    message = "Repeating current step"
    moved_back = False

    #After 2 times stuck on same step, move them back
    if progress.stuck_count >= 2 and progress.current_step > 0:
        progress.current_step -= 1
        progress.stuck_count = 0  # Reset stuck count after moving back
        moved_back = True
        message = "You seem stuck — let’s revisit the last step."


    # Check if already at the first step
    if progress.current_step == 0:
        return jsonify({
            "message": "You're already at the first step — let's try again together!"
        }), 200
    
    progress.stuck_count += 1
    db.session.commit()

    # Return the same instruction again
    step_texts = guide.step_texts or []
    current_instruction = ( step_texts[progress.current_step] if 0 <= progress.current_step < len(step_texts)else "No step found" )
    # print(f"[DEBUG] guide.step_texts: {guide.step_texts}")
    # print(f"[DEBUG] progress.current_step: {progress.current_step}")


    return jsonify({
        "message": message,
        "current_step": progress.current_step,
        "current_instruction": current_instruction,
        "moved_back": moved_back,
        "stuck_count": progress.stuck_count
    }), 200

#semi-tested
@guide_progress_routes.route('/progress/<vendor>', methods=['GET'])
@login_required
def get_guide_progress(vendor):
    """
    Get the current progress of the guide for the given vendor.
    """
    user_id = current_user.id
    vendor = vendor.strip()

    # Fetch guide and progress
    payment_guide = PaymentGuide.query.filter(PaymentGuide.user_id == current_user.id, PaymentGuide.vendor_name.ilike(vendor)).first()
    progress = GuideProgress.query.filter_by(user_id=user_id, vendor_name=vendor).first()

    if not payment_guide or not progress:
        return jsonify({"error": "Guide or progress not found"}), 404
    guide = progress.payment_guide
    step_text = guide.step_texts or []
    current_idx = progress.current_step

    #out of bounds safety
    if current_idx >= len(step_text):
        current_idx = len(step_text) - 1

    current_instrruction = (step_text[current_idx] if 0 <= current_idx < len(step_text) else "No step found")

    percent_complte = round((current_idx + 1) / len(step_text) * 100, 2) if step_text else 0
    
    return jsonify({
        "progress": progress.to_dict(),
        "current_instruction": current_instrruction,
        "step_number": current_idx + 1,
        "total_steps": len(step_text),
        "is_complete": progress.is_complete,
        "percent_complete": percent_complte
    })


#untested
@guide_progress_routes.route('/<vendor>/complete', methods=['POST'])
@login_required
def complete_guide(vendor):
    """
    Mark the guide for the given vendor as complete.
    """
    user_id = current_user.id
    guide_progress = GuideProgress.query.filter_by(user_id=user_id, vendor_name=vendor).first()

    if not guide_progress:
        return jsonify({"error": "Guide progress not found"}), 404

    # Mark the guide as complete
    guide_progress.is_complete = True

    db.session.commit()

    return jsonify(guide_progress.to_dict()), 200