from sqlalchemy.dialects.postgresql import JSONB

from app import db


class Scans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer())
    title = db.Column(db.String(100))
    author = db.Column(db.String(100))
    genre = db.Column(db.String(100))


def update_scan(scan):
    db.session.add(scan)
    db.session.commit()

def delete_scan(scan):
    db.session.delete(scan)
    db.session.commit()

