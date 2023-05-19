from flask import flash, redirect, render_template, url_for

from flaskblog import app
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account has been created for {form.username.data}", "success")
        return redirect(url_for("login_page"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "x@x.pl" and form.password.data == "x":
            flash(f"You have been logged in! ({form.password.data})", "success")
            return redirect(url_for("home_page"))
        else:
            flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)
