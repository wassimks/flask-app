from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
import os


app=Flask(__name__)
datab=SQLAlchemy(app)
login_M=LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///alchemy.db'
app.config['SECRET_KEY']='123654789963258741321456987'


# app.config.from_mapping(
#     SECRET_KEY='dev'
#     , DATABASE=os.path.join(app.instance_path, 'flaskApp.sqlite')
# )

""" def test(inp=2):
	marks=models.marks.query.filter_by(relative_user_id=2).all()
	print (marks)
	print(type(marks))
	for mark in marks:
		if inp == mark.relative_post_id:
			print(True)
			break """

from . import views 
from .views import test
