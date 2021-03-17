from flask import Flask, request, Blueprint, render_template, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from . import db
from .models import User

admin_app = Blueprint('admin', __name__)

admin = Admin(admin_app, name='my little admin', template_mode='bootstrap3')
#admin.add_view(ModelView(User, db.session))
