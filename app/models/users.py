from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    phone_number = db.Column(db.String(100), nullable=False)
    image_address = db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))
    fave_genres = db.Column(db.String(100))
    def __repr__(self):
        return f'<User {self.email}>'


def get_user(id) -> Users:
    return Users.query.filter_by(id=id).first()

def update_user(user_id, user):
    db.session.add(user)
    db.session.commit()