from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '95c0810c89f98d5feaf159bcb2692a88'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.app_context().push()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
