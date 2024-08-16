from fourplay import db, login_manager
from flask_login import UserMixin
from flask import app

@login_manager.user_loader
def load_user(volunteer_id):
    return Volunteer.query.get(int(volunteer_id))

class Volunteer(db.Model, UserMixin):
    volunteer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_id(self):
           return (self.volunteer_id)

    def __repr__(self):
        return f"User('{self.volunteer_id}', {self.username}', '{self.email}', '{self.password}')"

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Inventory('{self.item}', '{self.quantity}')"
    
# phone_no - primary key because we want him to come only once and we keep it for OTP. If phone_no exists in db, redirect to home page
# location is for determining red zone or not
class Victim(db.Model):
    phone = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    longitude = db.Column(db.Float, unique=True, nullable=False)
    latitude = db.Column(db.Float, unique=True, nullable=False)