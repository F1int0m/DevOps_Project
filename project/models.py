from . import db
from flask import redirect, url_for, request
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView

cart = db.Table('cart',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
                db.Column('count', db.Integer)
                )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean)
    cart = db.relationship('Item', secondary=cart, lazy='subquery', backref=db.backref('users', lazy=True))

    def __str__(self):
        return self.name + '*' if self.is_admin else ''


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(500))
    image_in_b64 = db.Column(db.Text)
    price = db.Column(db.Integer)
    is_ready = db.Column(db.Boolean)

    def __repr__(self):
        return self.name


class AdminView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index', next=request.url))

    def is_accessible(self):
        return current_user.is_admin
