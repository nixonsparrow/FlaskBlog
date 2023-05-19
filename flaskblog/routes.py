import os
import secrets
from PIL import Image
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from flaskblog import app, bcrypt, db
from flaskblog.forms import LoginForm, PostForm, RegistrationForm, UpdateAccountForm
from flaskblog.models import Post, User


@app.route("/")
@app.route("/home")
def home_page():
    page = request.args.get("page", 5, type=int)
    posts = Post.query.paginate(page=page, per_page=1)
    return render_template("home.html", posts=posts)


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
        try:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user=user, remember=form.remember.data)
                flash(f"{user.username}, you have been logged in!", "success")
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("home_page"))
        except ValueError:
            pass
        flash("Login unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for("home_page"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=["GET", "POST"])
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
        redirect(url_for("account_page"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created.", "success")
        return redirect(url_for("home_page"))
    return render_template("post_form.html", title="New Post", legend="New Post", form=form)


@app.route("/post/<int:post_id>", methods=["GET"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated.", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("post_form.html", title="Update Post", legend="Update Post", post=post, form=form)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home_page'))
