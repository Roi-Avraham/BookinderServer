import json

from app import db


class Chats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_person = db.Column(db.Integer)
    second_person = db.Column(db.Integer)


def get_all_contacts(user_id):
    contacts = []
    first = Chats.query.filter(Chats.first_person == user_id).all()
    second = Chats.query.filter(Chats.second_person == user_id).all()
    for row in first:
        contacts.append(row.second_person)
    for row in second:
        contacts.append(row.first_person)
    print("contatcs are:", contacts)
    return json.dumps(contacts)


