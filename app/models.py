from flask_login import UserMixin
from sqlalchemy import event

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    profile = db.relationship('Profile', back_populates='user',cascade='all, delete-orphan', uselist=False)
    products = db.relationship('Product', back_populates='seller', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def is_active(self):
        return True

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(255), default='media/profile_pics/default.png')  # Path to profile picture
    location = db.Column(db.String(100), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='profile')


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), nullable=True)  # Path to image
    location = db.Column(db.String(100), nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    category = db.relationship('Category', back_populates='products')
    seller = db.relationship('User', back_populates='products')

@event.listens_for(User, 'after_insert')
def create_user_profile(mapper, connection, target):
    profile = Profile(user=target)
    db.session.add(profile)
