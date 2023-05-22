# FLASK BLOG

Blog application created with Flask Framework (2.3.2) and SQLAlchemy.


## NOTES

### Initial info

To have default user image add `default.jpg` file into given folder:

```/ProjectName/flaskblog/static/profile_pics/```

### Database:

There is no `QuerySet` objects like in Django - methods return simple lists,
so there is no possible of chain commands.

Models are more directly created by SQL Alchemy than in Django.

#### Methods

To manipulate database inside the shell start with:
```
from flaskblog import app, db
app.app_context().push()
```
Then you can use all of below examples either in shell (or straight in code):
```
db.drop_all()
db.create_all()

Post.query.all()
Post.query.first()
Post.query.filter_by(user_id=1).all()

user = User(**some_user_data)
db.session.add(user)
post = Post(**some_post_data)
db.session.add(post)
db.session.commit()

db.session.add(wrong_post)
db.session.rollback()
```