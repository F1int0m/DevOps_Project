from . import db
from flask_login import UserMixin

cart = db.Table('cart',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
                )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    is_admin = db.Column(db.Boolean)
    cart = db.relationship('Item', secondary=cart, lazy='subquery', backref=db.backref('users', lazy=True))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    image_in_b64 = db.Column(db.Text)
    ready = db.Column(db.Boolean)
