from project import db, create_app
from project.models import User, Item, Cart
from werkzeug.security import generate_password_hash
from sqlalchemy import select

app = create_app()
db.init_app(app)
app.app_context().push()

res = db.session.query(Cart).filter(Cart.c.user_id == 1).filter(Cart.c.item_id==1)
d = Cart.delete().where(Cart.c.item_id==1).where(Cart.c.user_id==1213)
print(db.engine.execute(d))
print(res.all())
