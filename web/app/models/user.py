from app import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String)
    l_name = db.Column(db.String)
    email = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, f_name, l_name, email, role, ):
        self.firstname = f_name
        self.lastname = l_name
        self.email = email
        self.role = role

    def update(self, f_name, l_name, email, role, ):
        self.firstname = f_name
        self.lastname = l_name
        self.email = email
        self.role = role

