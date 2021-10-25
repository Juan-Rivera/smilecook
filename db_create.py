from app import db
import app

with app.app_context():
    db.create_all()
