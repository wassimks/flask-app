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

from . import views