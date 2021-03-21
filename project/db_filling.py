from project import db, create_app
from project.models import User, Item, Cart
from werkzeug.security import generate_password_hash
from sqlalchemy import select
import os

os.remove('db.sqlite')


def createProducts():
    list = [
        ['name', 'description', 'image', 11, False],
        ['prod 1', 'desc 1', 'image(', 10, True],
        ['Help', 'description', 'image((', 123, True],
        ['pls no', 'description', 'image(((', 32, False],
        ['U cool', 'description', 'image((((', 54, True],
        ['Hah, nope', 'description', 'image(((((', 765, True],
        ['name', 'description', 'image((((((', 1111, False]
    ]
    for item in list:
        db.session.add(Item(name=item[0], description=item[1], image_in_b64=item[2], price=item[3], is_ready=item[4]))


admin = User(name='Nikita', is_admin=True, email='buguev.nikita@gmail.com',
             password=generate_password_hash("123123", method='sha256'))
guest = User(id=11, name='And', email='123@c.com', password=generate_password_hash('123', method='sha256'))

app = create_app()
db.create_all(app=app)
db.init_app(app)
app.app_context().push()

db.session.add(admin)
db.session.add(guest)
createProducts()

ins = Cart.insert().values(user_id=11, item_id=3, count=10)
ins2 = Cart.insert().values(user_id=1, item_id=1, count=100)

db.session.commit()

db.engine.execute(ins)
db.engine.execute(ins2)
