from app import db
from sqlalchemy_serializer import SerializerMixin

class Document(db.Model, SerializerMixin):
    __tablename__ = "document"

    id = db.Column(db.Integer, primary_key=True)
    # subject = db.Column(db.String(300))
    doc_name = db.Column(db.String(300))
    doc_path = db.Column(db.String(300))
    user_id = db.Column(db.Integer)

    def __init__(self, doc_name, doc_path, u_id):
        self.doc_name = doc_name
        self.doc_path = doc_path
        self.user_id = u_id

    def update(self, doc_name, doc_path, u_id):
        self.doc_name = doc_name
        self.doc_path = doc_path
        self.user_id = u_id