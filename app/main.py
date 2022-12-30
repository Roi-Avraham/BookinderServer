from app import app, db
from users import Users
from books import Books
from rates import Rates
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
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

def login(msg_received):
    email = msg_received["username"]
    password = msg_received["password"]

    if (len(Users.query.filter_by(email=email, password =password).all()) == 0):
        return "failure"
    else:
        return "success"

@app.route('/addbookmanually', methods = ['GET', 'POST'])
def add_book_manually():
    msg_received = flask.request.get_json()
    current_user = msg_received["current_user"]
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
    user_id = Users.query.filter_by(email=current_user).first().id
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
    current_user = msg_received["current_user"]

    love_book = {}
    user_id = Users.query.filter_by(email=current_user).first().id
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


@app.route('/images/<image_name>', methods=['GET'])
def get_image(image_name):
    im_path = 'resources/images/' + image_name
    if os.path.exists(im_path):
        image = open(im_path, 'rb')
        # Send the image data back to the client
        return send_file(image, mimetype='image/png')
    return "failure"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

