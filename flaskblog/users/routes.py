import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.models import Post, User
from flaskblog.users.forms import LoginForm, RegistrationForm, UpdateAccountForm
from flaskblog.users.utils import save_picture

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("main.home_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created for you, {user.username}. You can now log in.", "success")
        return redirect(url_for("users.login_page"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user=user, remember=form.remember.data)
                flash(f"{user.username}, you have been logged in!", "success")
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("main.home_page"))
        except ValueError:
            pass
        flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("main.home_page"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account_page():
    form = UpdateAccountForm(username=current_user)
    if form.validate_on_submit():
        old_picture = None
        if form.picture.data:
            old_picture = url_for("static", filename="profile_pics/" + current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated.", "success")
        if old_picture and "default.jpg" not in old_picture:
            os.remove((app.root_path + old_picture).replace("/", "\\"))  # somehow os.path.join does not work here
        redirect(url_for("users.account_page"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)
