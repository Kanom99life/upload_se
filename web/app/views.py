import os
import hashlib
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from app import app, db
from app.models.document import Document

app.config['UPLOAD_FOLDER'] = 'static/files'
ALLOWED_EXTENSIONS = {'pdf'}

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[
        InputRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'Only PDF files are allowed.')
    ])
    submit = SubmitField("Upload File")

def generate_hash(path):
   
    hasher = hashlib.sha256()
    hasher.update(path.encode('utf-8'))
    return hasher.hexdigest()

  
@app.route('/', methods=['GET', 'POST'])
def main():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.root_path, file_path))

        hashed_path = generate_hash(file_path)
       
        new_document = Document(doc_path=hashed_path, u_id=1)  # Create a new Document instance and save it to the database
        db.session.add(new_document)
        db.session.commit()

        return "File has been uploaded."

    return render_template('main.html', form=form)
