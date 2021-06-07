from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_caching import Cache
import os, dotenv
from rq import Queue
from worker import conn

dotenv.load_dotenv()

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_HOST': os.getenv('redis_server'),
                      'CACHE_REDIS_PORT': os.getenv('redis_port')})
q = Queue(connection=conn)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ENV'] = os.getenv('FLAS_ENV')
    db.init_app(app)

    cache.init_app(app)

    from app.redis_queue import send_email

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Item, Cart, AdminView
    admin = Admin(app)
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Item, db.session))

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except:
            return None


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .items_catalog import catalog_app as catalog_blueprint
    app.register_blueprint(catalog_blueprint)

    return app
