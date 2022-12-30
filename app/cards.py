from app import db


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    image_address = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float)


def get_card(id):
    return Cards.query.filter_by(id=id).first()
