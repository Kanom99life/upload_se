import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for
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

        # Save the filename (doc_name) to the database
        new_document = Document(doc_name=filename, doc_path=hashed_path, u_id=1)
        db.session.add(new_document)
        db.session.commit()
       

    # Query the database to get the list of uploaded documents
    documents = Document.query.all()

    return render_template('main.html', form=form, documents=documents)



@app.route('/rename_document/<int:document_id>', methods=['GET', 'POST'])
def rename_document(document_id):
    document = Document.query.get(document_id)

    if document is None:
        # Handle the case where the document with the given ID does not exist
        return "Document not found", 404

    if request.method == 'POST':
        new_name = request.form.get('new_name')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.doc_name)
        if new_name:
            # Get the document's current path
            current_path = os.path.join(app.root_path, file_path)
            # print("current_path = ", current_path)
            # Get the new filename and path
            new_filename = secure_filename(new_name + ".pdf") # Add ".pdf" because after rename file it remove .pdf So that, pdf file will broke.
            new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

            try:
                # Rename the file on the file system
                os.rename(current_path, new_path)

                # Update the document's name and hashed path in the database
                document.doc_name = new_filename
                document.doc_path = generate_hash(new_path)
                db.session.commit()

                return redirect(url_for('main'))

            except OSError:
             
                return "Error renaming the document"

  
    return render_template('rename_document.html', document=document)