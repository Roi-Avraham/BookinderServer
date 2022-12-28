from app import db


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    writer_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(80))

    def __repr__(self):
        return f'<Book {self.name}>'


def get_book(id):
    return Books.query.filter_by(id=id).first()


def get_book_by_name_and_writer(name, writer):
    return Books.query.filter_by(name=name, writer_name=writer).first()
