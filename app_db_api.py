from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import flask_restless
from os import environ

app = Flask(__name__)
api = Api(app)



app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
