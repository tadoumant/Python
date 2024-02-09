#Tables DataBase

from datetime import datetime
from gtaches import db,login_manager
from flask_login import UserMixin

#for login
@login_manager.user_loader
def load_admin(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    #category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    #taches_id = db.Column(db.Integer, db.ForeignKey("taches.id"), nullable=True)


    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"


class Taches(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(20), nullable=False, default="default_thumbnail.jpg")
    #tache = db.relationship("Taches", backref="tache_name", lazy=True)

    def __repr__(self):
        return f"Tache('{self.title}', '{self.date_posted}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
   # tache = db.relationship("Taches", backref="tache_name", lazy=True)

    def __repr__(self):
        return f"Category('{self.title}')"



# class Admin(db.Model,UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     fname = db.Column(db.String(25), nullable=False)
#     lname = db.Column(db.String(25), nullable=False)
#     username = db.Column(db.String(25), unique=True, nullable=False)
#     email = db.Column(db.String(125), unique=True, nullable=False)
#     image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
#     password = db.Column(db.String(60), nullable=False)
#     users = db.relationship("User", backref="author", lazy=True)
    
#     def __repr__(self):
#         return f"Admin('{self.fname}', '{self.lname}', '{self.username}', '{self.email}', '{self.image_file}')"
