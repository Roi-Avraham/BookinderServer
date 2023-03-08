import json

from app import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer)
    receiver = db.Column(db.Integer)
    message = db.Column(db.String(100))

def get_all_messages(user_one, user_two):
    messages = []
    rows = Messages.query.filter((Messages.sender == user_one and Messages.receiver == user_two)
                                 or (Messages.sender == user_two and Messages.receiver == user_one)).all()
    for row in rows:
        messages.insert(row.id)
    return json.dumps(messages)


def get_message(id):
    return Messages.query.filter_by(id=id).first()