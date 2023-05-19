from flask import Flask, render_template, url_for

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True)
