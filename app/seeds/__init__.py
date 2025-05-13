from flask.cli import AppGroup
from .document import seed_documents_for_nlp, undo_documents
from .user import seed_users, undo_users
from .payment_guide import seed_payment_guides_for_vendors, undo_payment_guides

from app.models.db import db, environment

seed_commands = AppGroup('seed')

@seed_commands.command('all')
def seed():
    if environment == "production":
        undo_documents()
        undo_payment_guides()
        undo_users()

    # Step 1: Seed users and capture them
    users = seed_users()

    # Step 2: Use one user's ID (e.g., 'demo') for the guides/docs
    user_id = users["demo"].id

    # Step 3: Seed guides and pass the user_id
    guide_map = seed_payment_guides_for_vendors(user_id=user_id)

    # Step 4: Seed documents and pass both user_id and guide_map
    seed_documents_for_nlp(user_id=user_id, guide_map=guide_map)

    print("Seeding complete!")

@seed_commands.command('undo')
def undo():
    if environment == "production":
        undo_users()
        undo_payment_guides()
        undo_documents()
    print("Undoing complete!")