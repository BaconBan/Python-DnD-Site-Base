from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
import random

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dungeons.db'

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    charName = db.Column(db.String(40), nullable=False)
    charRace = db.Column(db.String(40), nullable=False)
    charClass = db.Column(db.String(40), nullable=False)
    strength = db.Column(db.Integer, nullable=False)
    dexterity = db.Column(db.Integer, nullable=False)
    intelligence = db.Column(db.Integer, nullable=False)
    constitution = db.Column(db.Integer, nullable=False)
    wisdom = db.Column(db.Integer, nullable=False)
    charisma = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = 'DnD is over 50 years old'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user

@app.route('/')
def index():
    return render_template('Main Template.html')

@app.route('/loginuser', methods=['GET', 'POST'])
def login():
    error = 3 #Not logged in
    if request.method == 'GET':
        return render_template('loginuser.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user is None:
            #No User
            return render_template('loginuser.html', user = 'User')
        elif user.password == password:
            login_user(user)
            #No Error
            return render_template('Main Template.html', user='Logged')
        else:
            #Wrong Password
            return render_template('loginuser.html', user='Password')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Main Template'))

@app.route('/createuser', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createuser.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['charName']
        race = request.form['race']
        charClass = request.form['class']
        strength = random.randint(10, 20)
        dexterity = random.randint(10, 20)
        constitution = random.randint(10, 20)
        intelligence = random.randint(10, 20)
        wisdom = random.randint(10, 20)
        charisma = random.randint(10, 20)
        if username != User.query.filter_by(username=username).all():
            user = User(username=username, password=password, strength=strength, dexterity=dexterity,
            constitution=constitution, intelligence=intelligence, wisdom=wisdom, charisma=charisma, charClass=charClass, charName=name, charRace=race)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main'))
        else:
            return render_template('createuser.html', error='Password')

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'GET':
        return render_template('update.html')
    elif request.method == 'POST':
        password = request.form['oldPassword']

        if password != current_user.password:
            error = 1 #Not right password
            return render_template('update.html', error='Password')
        else:
            current_user.password = request.form['newPassword']
            db.session.commit()
            return redirect(url_for('main'))

app.run(debug=True)