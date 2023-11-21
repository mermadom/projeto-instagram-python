# Aqui vai as rotas e links
import os

from flask import flash, get_flashed_messages, render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename

from instagram.models import Friendship, load_user, User, Posts
from instagram import app, database
from instagram.forms import FormLogin, FormCreateNewAccount, FormCreateNewPost
from instagram import bcrypt
from instagram import login_manager


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
def homepage():
    formLogin = FormLogin()
    users = User.query.all()

    if formLogin.validate_on_submit():
        userToLogin = User.query.filter_by(email=formLogin.email.data).first()
        if userToLogin and bcrypt.check_password_hash(userToLogin.password, formLogin.password.data):
            login_user(userToLogin)
            return redirect(url_for('profile', user_id=userToLogin.id))


    return render_template("home.html", teto='HOME', form=formLogin,users=users)


@app.route('/profile/<user_id>', methods=['POST', 'GET'])
@login_required
def profile(user_id):
    users = User.query.all()
    if int(user_id) == int(current_user.id):
        # estou vendo meu perfil
        _formNewPost = FormCreateNewPost()

        if _formNewPost.validate_on_submit():
            # pegar o texto
            _post_text = _formNewPost.text.data

            # pegar a img
            _post_img = _formNewPost.photo.data
            _img_name = secure_filename(_post_img.filename)
            path = os.path.abspath(os.path.dirname(__file__))
            path2 = app.config['UPLOAD_FOLDER']
            _final_path = f'{path}/{path2}/{_img_name}'

            _post_img.save(_final_path)

            # criar um obj Post
            newPost = Posts(post_text=_post_text,
                           post_img=_img_name,
                           user_id=int(current_user.id)
                           )

            # salvar no banco
            database.session.add(newPost)
            database.session.commit()

        return render_template("profile.html", user=current_user, form=_formNewPost, users=users)
    else:
        # outro perfil"""
        _user = User.query.get(int(user_id))
        friendships = Friendship.query.filter(Friendship.user_id == int(current_user.id),Friendship.friend_id == int(user_id)).first()
        if friendships:
            return render_template("profile.html", user=_user, form=False, users=users,blocked = friendships.blocked)
        else:
            return render_template("profile.html", user=_user, form=False, users=users,blocked = False) 


@app.route('/capaivara')
def capaivara():
    return render_template("capaivara.html")


@app.route('/teste')
def teste():
    return render_template("teste.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/new', methods=['POST', 'GET'])
def create_account():
    formCreateAccount = FormCreateNewAccount()

    if formCreateAccount.validate_on_submit():
        password = formCreateAccount.password.data
        password_cr = bcrypt.generate_password_hash(password)
        # print(password)
        # print(password1)

        newUser = User(username=formCreateAccount.username.data,
                       email=formCreateAccount.email.data,
                       password=password_cr)

        database.session.add(newUser)
        database.session.commit()
        login_user(newUser, remember=True)
        return redirect(url_for('profile', user_id=newUser.id))

    return render_template("new.html", form=formCreateAccount)

@app.route('/profile/<user_id>/like/<int:post_id>', methods=['POST'])
def like(user_id,post_id):
    post = Posts.query.get_or_404(post_id)
    post.likes += 1
    database.session.commit()
    flash('Você curtiu o post!', 'success')
    return redirect(url_for('profile', user_id=user_id))

@app.route('/block/<int:friend_id>', methods=['POST'])
def block(friend_id):
    user = User.query.get_or_404(int(current_user.id))
    friend = User.query.get_or_404(friend_id)

    # Verifica se já existe uma amizade registrada
    friendship = Friendship.query.filter_by(user_id=user.id, friend_id=friend.id).first()

    if not friendship:
        # Se não houver uma amizade registrada, cria uma nova amizade
        friendship = Friendship(user_id=user.id, friend_id=friend.id)
        database.session.add(friendship)

    # Bloqueia ou desbloqueia o amigo
    friendship.blocked = not friendship.blocked

    database.session.commit()
    flash(f'Você {"bloqueou" if friendship.blocked else "desbloqueou"} o perfil de {friend.username}!', 'success')
    return redirect(url_for('profile', user_id=int(friend_id)))
