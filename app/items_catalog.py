from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from jsonrpc import dispatcher
from .models import Item, User, Cart
from . import db, models, cache
from .redis_queue import remind_old_order
from .order import get_cart

catalog_app = Blueprint('catalog', __name__)


@catalog_app.route('/cart')
@login_required
def cart():
    user_id = current_user.id

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    items = get_cart(user_id)
    return render_template('cart.html', items=items)


@catalog_app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    items = Item.query.filter_by(is_ready=True).all()
    return render_template('catalog.html', items=items, user=current_user)


@catalog_app.route('/secretCatalog', methods=['GET', 'POST'])
def secretCatalog():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    items = Item.query.all()
    return render_template('catalog.html', items=items, user=current_user)


@dispatcher.add_method
def add_to_cart(item_id, count):
    checked_count = check_count(count)
    checked_item_id = check_item_id(item_id)

    if type(checked_count) is not int or type(checked_item_id) is not int:
        return {'text': 'Bad number', 'item_id': checked_item_id, 'count': checked_count}

    res = db.session.query(Cart).filter(Cart.c.item_id == checked_item_id) \
        .filter(Cart.c.user_id == current_user.id).first()
    if res is None:
        ins = Cart.insert().values(user_id=current_user.id, item_id=checked_item_id, count=checked_count)
        db.engine.execute(ins)
    else:
        stmt = Cart.update(). \
            values(count=(Cart.c.count + checked_count)). \
            where(Cart.c.item_id == checked_item_id). \
            where(Cart.c.user_id == current_user.id)
        db.engine.execute(stmt)
    cache[current_user.id] = None
    remind_old_order(current_user.id, get_cart(current_user.id))
    return 'OK'


@dispatcher.add_method
def remove_from_cart(item_id):
    checked_item_id = check_item_id(item_id)
    if type(checked_item_id) is not int:
        return {'text': 'Bad Number', 'item_id': checked_item_id}
    stmt = Cart.delete().where(Cart.c.item_id == checked_item_id) \
        .where(Cart.c.user_id == current_user.id)
    db.engine.execute(stmt)
    return 'OK'


def check_item_id(id):
    try:
        item_id = int(id)
        if Item.query.filter_by(id=item_id).count() > 0:
            return item_id
        return {'text': 'Item not found', 'item_id': id}
    except:
        return {'text': 'Bad id', 'item_id': id}


def check_count(value):
    try:
        count = int(value)
        if count > 0:
            return count
    except:
        return {'text': 'Bad count', 'count': value}
