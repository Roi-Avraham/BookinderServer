from app import db
from app.models.books import get_book_by_name_and_writer
from app.utils import image_to_url


class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    image_address = db.Column(db.String(100))
    method = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float)


def get_card(id) -> Cards:
    return Cards.query.filter_by(id=id).first()


def get_all_by_method_and_user(method, user_id):
    return Cards.query.filter_by(user_id=user_id, method=method).all()


def upload_book(msg_received, image, host):
    user_id = msg_received["user_id"]
    name_of_book = msg_received["name_of_book"]
    name_of_writer = msg_received["name_of_writer"]
    method = msg_received["method"]
    genre = msg_received["genre"]
    if method == "sale":
        price = float(msg_received["price"])
    elif method == "exchange":
        price = 0.0
    else:
        return "failure: expected \"selling\" or \"exchange\" in method name"
    book_id = get_book_by_name_and_writer(name_of_book, name_of_writer,genre).id
    book_card = Cards(user_id=user_id, book_id=book_id, method=method, price=price)
    db.session.add(book_card)
    db.session.commit()
    book_card.image_address = image_to_url(image,'book', book_card.book_id, host)
    db.session.add(book_card)
    db.session.commit()
    return book_card


def get_all_cards_for_user(user_id):
    return Cards.query.all()
