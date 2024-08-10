from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(volunteer_id):
    return Volunteer.query.get(int(volunteer_id))

bcrypt = Bcrypt(app)

app.app_context().push()

class Volunteer(db.Model, UserMixin):
    volunteer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def get_id(self):
           return (self.volunteer_id)

    def __repr__(self):
        return f"User('{self.volunteer_id}', {self.username}', '{self.email}', '{self.password}')"

class inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# phone_no - primary key because we want him to come only once and we keep it for OTP. If phone_no exists in db, redirect to home page
# location is for determining red zone or not
class Victim(db.Model):
    phone_no = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        volunteer = Volunteer(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(volunteer)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        volunteer = Volunteer.query.filter_by(email=form.email.data).first()
        if volunteer:
            if bcrypt.check_password_hash(volunteer.password, form.password.data):
                login_user(volunteer)
                return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html', form=form)

# Remove while deploying
if __name__ == '__main__':
    app.run(debug=True)
