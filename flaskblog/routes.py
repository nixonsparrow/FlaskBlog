from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.forms import LoginForm, RegistrationForm
from flaskblog.models import Post, User


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=Post.query.all())


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for("home_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account has been created for you, {user.username}. You can now log in.", "success")
        return redirect(url_for("login_page"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user=user, remember=form.remember.data)
            flash(f"{user.username}, you have been logged in!", "success")
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home_page"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("home_page"))


@app.route("/account", methods=["GET"])
@login_required
def account_page():
    return render_template("account.html", title="Account")
