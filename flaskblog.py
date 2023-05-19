from flask import flash, Flask, redirect, render_template, url_for
from forms import LoginForm, RegistrationForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "InseCuresecretKey123456!@#$%^"

posts = [
    {
        "author": "Nikodem Wróbel",
        "title": "Blog post 1",
        "content": "This is the first blog post",
        "date_posted": "May 19, 2023"
    },
    {
        "author": "Nikodem Wróbel",
        "title": "Blog post 2",
        "content": "This is the second blog post",
        "date_posted": "May 20, 2023"
    }
]


@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html", posts=posts)


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


if __name__ == '__main__':
    app.run(debug=True)
