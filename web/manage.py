from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.document import Document

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(Document(doc_name="ทดสอบ, test", doc_path= "111111111", u_id=0))

    db.session.commit()



if __name__ == "__main__":
    cli()
