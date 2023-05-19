# FLASK BLOG

Blog application created with Flask Framework (2.3.2) and SQLAlchemy.


## NOTES

### Database:

There is no `QuerySet` objects like in Django - methods return simple lists,
so there is no possible of chain commands.

Models are more directly created by SQL Alchemy than in Django.

#### Methods
```
Post.query.all()
Post.query.first()
Post.query.filter_by(user_id=1).all()

post = Post(**post_data)
db.session.add(post)
db.session.commit()

db.session.add(wrong_post)
db.session.rollback()

db.create_all()
db.drop_all()
```