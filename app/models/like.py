from app import db


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    card_id = db.Column(db.Integer, nullable=False)

def _get_like(user_id, card_id):
    return Likes.query.filter_by(user_id=user_id, card_id=card_id).first()

def is_liked(user_id, card_id):
    return _get_like(user_id, card_id) is not None


def add_like(user_id, card_id):
    if not is_liked(user_id, card_id):
        like = Likes(user_id=user_id, card_id=card_id)
        db.session.add(like)
        db.session.commit()

def cancel_like(user_id, card_id):
    like = _get_like(user_id, card_id)
    if like is not None:
        db.session.delete(like)
        db.session.commit()

def get_all_user_likes(user_id):
    likes = Likes.query.filter_by(user_id=user_id).all()
    cards = [like.card_id for like in likes]
    return cards
