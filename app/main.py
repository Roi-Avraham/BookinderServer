from app import app, db, HOST
import flask
from app.models import Users, Books, Rates, Cards
from app.models.cards import upload_book, get_card, get_all_by_method_and_user
from app.models.books import get_book
from app.models.users import get_user, update_user
from flask import send_file, json, request
from utils import image_to_url
import os
############################################################################
with app.app_context():
    db.drop_all()
    db.create_all()
########################################################################
@app.route('/', methods = ['GET', 'POST'])
def start():
    msg_received = flask.request.get_json()
    msg_subject = msg_received["subject"]

    if msg_subject == "register":
        return register(msg_received)
    elif msg_subject == "login":
        return login(msg_received)
    else:
        return "Invalid request."

def register(msg_received):
    name = msg_received["name"]
    email = msg_received["email"]
    password = msg_received["password"]
    phone = msg_received["phone"]
    age = msg_received["age"]

    if(len(Users.query.filter_by(email=email).all()) != 0):
        return "Another user used this email. Please chose another email."
    user = Users(name=name, email=email, password=password, phone_number=phone,age=age)
    try:
        db.session.add(user)
        db.session.commit()
        return str(user.id)
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

def login(msg_received):
    email = msg_received["username"]
    password = msg_received["password"]
    user = Users.query.filter_by(email=email, password =password).first()
    if user is None:
        return "failure"
    else:
        return str(user.id)

@app.route('/addbookmanually', methods = ['GET', 'POST'])
def add_book_manually():
    msg_received = flask.request.get_json()
    user_id = msg_received["current_user"]
    name_of_book = msg_received["name_of_book"]
    name_of_writer = msg_received["name_of_writer"]
    genre = msg_received["genre"]
    rate = msg_received["rate"]

    if (len(Books.query.filter_by(name=name_of_book).all()) == 0):
        new_book = Books(name=name_of_book, writer_name=name_of_writer, genre=genre)
        try:
            db.session.add(new_book)
            db.session.commit()
        except Exception as e:
            print("Error while inserting the new record :", repr(e))
            return "failure"
    book_id = Books.query.filter_by(name = name_of_book).first().id
    new_rate = Rates(user_id=user_id, book_id=book_id, rate=rate)
    try:
        db.session.add(new_rate)
        db.session.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

@app.route('/getBooksYouEntered', methods = ['GET', 'POST'])
def get_books_you_entered():
    msg_received = flask.request.get_json()
    user_id = msg_received["current_user"]

    love_book = {}
    all_rates = Rates.query.filter_by(user_id=user_id).all()
    if(len(all_rates) != 0):
        index = 0
        love_book["number"] = str(len(all_rates))
        for element in all_rates:
            name_of_book = Books.query.filter_by(id=element.book_id).first().name
            name_of_writer = Books.query.filter_by(id=element.book_id).first().writer_name
            genre = Books.query.filter_by(id=element.book_id).first().genre
            love_book["name_of_book" + str(index)] = name_of_book
            love_book["name_of_writer" + str(index)] = name_of_writer
            love_book["genre" + str(index)] = genre
            love_book["rate" + str(index)] = element.rate
            index = index + 1
    return json.dumps(love_book)


@app.route('/images/<image_name>',methods=['GET'])
def get_image(image_name):
    im_path = os.path.join('..','resources', 'images', image_name)
    #im_path = 'resources/images/' + image_name
    if os.path.exists(im_path):
        image = open(im_path, 'rb')
        # Send the image data back to the client
        return send_file(image, mimetype='image/png')
    return "failure", 404


@app.route('/upload_book', methods=['POST'])
def upload_book_route():
    book_data = request.form['card']
    image = request.files['image']
    host = request.headers['Host']
    book_card = upload_book(json.loads(book_data), image, host)
    return str(book_card.id)


@app.route('/update_profile_pic/<int:user_id>', methods=['POST'])
def update_profile(user_id):
    image = request.files['image']
    host = request.headers['Host']
    user = get_user(user_id)
    user.image_address = image_to_url(image, "profile", user_id, host)
    update_user(user_id, user)
    return "success"


@app.route('/items/<int:card_id>',methods=['POST'])
def get_card_route(card_id):
    card = get_card(card_id)
    book_id = card.book_id
    seller_id = card.user_id
    book = get_book(book_id)
    seller = get_user(seller_id)
    dic = {
        'title': str(book.name),
        'author': str(book.writer_name),
        'book_image': str(card.image_address),
        'method': str(card.method),
        'price': str(card.price),
        'genre': str(book.genre),
        'seller_id': str(seller_id),
        'seller_name': str(seller.name),
        'seller_image': str(seller.image_address)
    }
    return json.dumps(dic)


@app.route('/items/exchange/<int:user_id>',methods=['POST'])
def get_cards_exchange(user_id):
    all_cards = get_all_by_method_and_user('exchange', user_id)
    lst = [card.id for card in all_cards]
    return json.dumps(lst)

@app.route('/items/sale/<int:user_id>',methods=['POST'])
def get_cards_sale(user_id):
    all_cards = get_all_by_method_and_user('sale', user_id)
    lst = [card.id for card in all_cards]
    return json.dumps(lst)


@app.route('/profile/<int:user_id>',methods=['POST'])
def get_user_route(user_id):
    user = get_user(user_id)
    dic = {
        'name': user.name,
        'age': str(user.age),
        'phone': str(user.phone_number),
        'mail': str(user.email),
        'genres': user.fave_genres,
        'image_address': str(user.image_address)
    }
    return json.dumps(dic)
@app.route('/genres/<int:user_id>', methods=['POST'])
def upload_genres(user_id):
    msg_received = flask.request.get_json()
    genres = msg_received["genres"]
    user = get_user(user_id)
    user.fave_genres = genres
    update_user(user_id,user)
    return "success"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=HOST, debug=True, threaded=True)

