from instagram import database, app
from instagram.models import User, Posts

with app.app_context():
    database.create_all()
# só
