from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from . import db, models

catalog_app = Blueprint('catalog', __name__)


@catalog_app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    items = models.User.query.filter_by(id=current_user.id).first().cart
    return render_template('cart.html', items=items)


@catalog_app.route('/catalog')
def catalog():
    items = models.Item.query.filter_by(is_ready=True).all()
    return render_template('catalog.html', items=items, flag=False)


@catalog_app.route('/secretCatalog')
def secretCatalog():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    items = models.Item.query.all()
    return render_template('catalog.html', items=items, flag=True)
