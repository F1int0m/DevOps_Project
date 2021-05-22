from app import db, create_app
from app.models import User, Item
from werkzeug.security import generate_password_hash
import os

os.remove('app/db.sqlite')


def createProducts():
    list = [
        ['name', 'description', 'image', 11, False],
        ['Турболет', 'Летает быстро, но не очень', 'image(', 1000, True],
        ['Табурет', 'Вроде не летает', 'image((', 123, True],
        ['Котел "Василиса"', 'Жарит как надо', 'image(((', 32, False],
        ['Сверло 74', 'Говорят им сверлили самого Ленина', 'image((((', 54, True],
        ['Hah, nope', 'description', 'image(((((', 765, True],
        ['name', 'description 23', 'image((((((', 1111, False]
    ]
    for item in list:
        db.session.add(Item(name=item[0], description=item[1], image_in_b64=item[2], price=item[3], is_ready=item[4]))


admin = User(name='Nikita', is_admin=True, email='buguev.nikita@gmail.com',
             password=generate_password_hash(os.getenv('password'), method='sha256'))
app = create_app()
db.create_all(app=app)
db.init_app(app)
app.app_context().push()

db.session.add(admin)
createProducts()

db.session.commit()
