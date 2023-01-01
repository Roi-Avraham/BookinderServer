from app import db


class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<Rate {self.rate}>'

