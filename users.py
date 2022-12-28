from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'


def get_user(id):
    return Users.query.filter_by(id=id).first()
