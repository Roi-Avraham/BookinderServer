import os

import flask
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    "mysql://root:toor@localhost:3306/db_bookinder"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
############################################################################
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    writer_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Book {self.name}>'

class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Rate {self.rate}>'


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

    all_love_books = [[]]
    love_book = []
    user_id = Users.query.filter_by(email=current_user).first().id
    all_rates = Rates.query.filter_by(id=user_id).all()
    for element in all_rates:
        name_of_book = Books.query.filter_by(id=element.book_id).first().name
        name_of_writer = Books.query.filter_by(id=element.book_id).first().writer_name
        genre = Books.query.filter_by(id=element.book_id).first().genre
        love_book.append(name_of_book)
        love_book.append(name_of_writer)
        love_book.append(genre)
        love_book.append(element.rate)
        all_love_books.append(love_book)
    return jsonify({"all_love_books": all_love_books})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)

