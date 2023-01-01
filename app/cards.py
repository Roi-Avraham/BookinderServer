from app import db, HOST

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    image_address = db.Column(db.String(100), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float)


def get_card(id):
    return Cards.query.filter_by(id=id).first()

def upload_book(msg_received, image, host):
    user_id = msg_received['user_id']
    name_of_book = msg_received["name_of_book"]
    name_of_writer = msg_received["name_of_writer"]
    method = msg_received["method"]
    if method == "selling":
        price = float(msg_received["price"])
    elif method == "exchange":
        price = 0.0
    else:
        return "failure: expected \"selling\" or \"exchange\" in method name"
    book = Books.query.filter_by(name=name_of_book, writer_name=name_of_writer).first()
    if book is not None:
        book_id = book.id
    else:
        book = Books(name=name_of_book, writer_name=name_of_writer)
        if msg_received["genre"] != "None":
            book.genre = msg_received["genre"]
        try:
            db.session.add(book)
            db.session.commit()
            book_id = book.id
        except Exception as e:
            print("Error while inserting the new record :", repr(e))
            return "failure"
    filepath = f'{user_id}_{book_id}_{datetime.now()}_{img.name}'
    img.save(f'resources/books/{filepath}')
    book_inventory = BookInventory(user_id=user_id, book_id=book_id, method=method, price=price, img_addr=filepath)
    try:
        db.session.add(book_inventory)
        db.session.commit()
        return jsonify()
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"
