from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired, FileField

class DocumentForm(FlaskForm):
    image = FileField("Upload Image", validators=[
        FileRequired(message="Image is required."),
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], "Only images are allowed.")
    ])
    