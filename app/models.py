from datetime import datetime
from app import datab, login_M
from flask_login import UserMixin

@login_M.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users (datab.Model, UserMixin):
    id= datab.Column(datab.Integer(), primary_key=True)
    username= datab.Column(datab.String(length=50) )
    password= datab.Column(datab.String(length=255))

class posts (datab.Model):
    id= datab.Column(datab.Integer(), primary_key=True)
    date= datab.Column(datab.String(255), default=datetime.utcnow())
    post_title= datab.Column(datab.String(length=50) )
    post_body= datab.Column(datab.String(length=255))
    relative_index= datab.Column(datab.Integer(), datab.ForeignKey(users.id))
    average_mark= datab.Column(datab.Integer())

class comments(datab.Model):
    id= datab.Column(datab.Integer(), primary_key=True)
    date= datab.Column(datab.String(255), default=datetime.utcnow())
    commenter= datab.Column(datab.Integer(), datab.ForeignKey(users.id))
    original_post= datab.Column(datab.Integer(), datab.ForeignKey(posts.id))
    c_content= datab.Column(datab.String(255))

""" class likes(datab.Model):
    id= datab.Column(datab.Integer(), primary_key=True)
 """

class marks(datab.Model):
    id= datab.Column(datab.Integer(), primary_key=True)
    mark= datab.Column(datab.Integer())
    relative_user_id= datab.Column(datab.Integer(), datab.ForeignKey(users.id))
    relative_post_id= datab.Column(datab.Integer(), datab.ForeignKey(posts.id))