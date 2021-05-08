from . import db
from flask import redirect, url_for, request
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
import datetime, json

Cart = db.Table('cart',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True),
                db.Column('count', db.Integer, default=1)
                )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean)
    Cart = db.relationship('Item', secondary=Cart, lazy='subquery', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return 'T:' + self.name + '*' if self.is_admin else ''


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(500))
    image_in_b64 = db.Column(db.Text)
    price = db.Column(db.Integer)
    is_ready = db.Column(db.Boolean)

    def __repr__(self):
        return 'T:' + self.name

    @property
    def json(self):
        return to_json(self, self.__class__)


class AdminView(ModelView):
    create_modal = True
    edit_modal = True
    can_export = True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index', next=request.url))

    def is_accessible(self):
        return current_user.is_admin


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return json.dumps(d)
