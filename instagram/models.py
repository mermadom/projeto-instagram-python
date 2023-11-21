# Vai as classes / estrura do banco de dados
from instagram import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship("Posts", backref='user', lazy=True)
    friendships = database.relationship('Friendship', back_populates='user', foreign_keys='Friendship.user_id')


class Posts(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    post_text = database.Column(database.String, default='')
    post_img = database.Column(database.String, default='default.png')
    creation_date = database.Column(database.String, nullable=False, default=datetime.utcnow())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    likes = database.Column(database.Integer, default=0)

class Friendship(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    friend_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    blocked = database.Column(database.Boolean, default=False)
    user = database.relationship('User', foreign_keys=[user_id])
    friend = database.relationship('User', foreign_keys=[friend_id])