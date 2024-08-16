from flask import render_template, url_for, flash, redirect, request
from fourplay import app, db, bcrypt
from fourplay.forms import RegistrationForm, LoginForm
from fourplay.models import Volunteer, Inventory, Victim
from flask_login import login_user, current_user, logout_user, login_required

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
                return redirect(url_for('contributor'))
        else:
            return redirect(url_for('register'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/contributor', methods=['GET','POST'])
@login_required
def contributor():
    items = ['Food (Packets)', 'Clean Water Cans', 'Clothes', 'Bedspreads', 'Bed', 'Vessels','Medicines','Other: ']
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = int(request.form.get('quantity'))

        # check if exists
        exists = Inventory.query.filter_by(item=item).first()

        if exists:
            exists.quantity += quantity
        else:
            new_item = Inventory(item=item, quantity=quantity)
            db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('rec_cont'))
    inv = Inventory.query.all()
    return render_template('contributor.html', inv=inv, items=items)

@app.route("/receiver", methods=["POST", "GET"])
def receiver():
    '''
    if request.method == 'POST':
        phone = request.form.get('phone')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude') 

        if latitude and longitude:
            victim_data = Victim(phone=phone, latitude=float(latitude), longitude=float(longitude))
            db.session.add(victim_data)
            db.session.commit()
    '''
    return render_template('receiver.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')


@app.route("/rec_after")
def rec_after():
    return render_template('rec_after.html')

@app.route("/rec_cont")
@login_required
def rec_cont():
    inv = Inventory.query.all()
    return render_template('rec_cont.html', inv=inv)
