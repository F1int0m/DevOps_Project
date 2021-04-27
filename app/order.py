from .messages_module import send_email as smtp_send
from flask_login import current_user
from . import cache, db
from .models import Item, Cart


def check_order(user_id, cart):
    if cart == get_cart(user_id):
        smtp_send(current_user.email, 'changed', 'text')
    smtp_send(current_user.email, 'not changed', 'text')



def get_cart(user_id):
    if user_id in cache.keys() and cache[user_id] is not None:
        items = cache[user_id]
    else:
        items = db.session.query(Item, Cart).filter(Item.id == Cart.c.item_id).filter(Cart.c.user_id == user_id).all()
        cache[user_id] = items
    return items
