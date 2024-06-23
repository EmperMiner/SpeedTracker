from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from flask_bcrypt import Bcrypt
import time
import numpy as np

app = Flask(__name__,template_folder='templates')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    vehicleName = db.Column(db.String(20), nullable=False, unique=True)
    speedLimit = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(80), nullable=False, unique=True)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Log In')
    
class UserLoginForm(FlaskForm):
    code = StringField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Code"})
    submit = SubmitField('Enter')
    
class VehicleForm(FlaskForm):
    vehicleName = StringField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Vehicle Name"})

    speedLimit = IntegerField(validators=[
                             InputRequired(), NumberRange(min=1, max=200)], render_kw={"placeholder": "Speed Limit (m/s)"})

    code = StringField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Code (for user)"})

    submit = SubmitField('Register')

    def validate_vehicleName_code(self, vehicleName, code):
        existing_vehicle_vehicleName = Vehicle.query.filter_by(
            vehicleName=vehicleName.data).first()
        if existing_vehicle_vehicleName:
            raise ValidationError(
                'That vehicle name already exists. Please choose a different one.')
        existing_vehicle_code = Vehicle.query.filter_by(
            code=code.data).first()
        if existing_vehicle_code:
            raise ValidationError(
                'That code already exists. Please choose a different one.')
        

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/userLogin', methods=['GET', 'POST'])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
            
        codeExists = Vehicle.query.filter_by(code=form.code.data).first()
        if codeExists:
            return redirect(url_for("vehicle", code=form.code.data ))
    return render_template('userLogin.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = VehicleForm()
    
    if form.validate_on_submit():
        new_vehicle = Vehicle(username=current_user.username,vehicleName=form.vehicleName.data,speedLimit=form.speedLimit.data,code=form.code.data)
        db.session.add(new_vehicle)
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    try:
        vehicles = db.session.execute(db.select(Vehicle)
            .filter_by(username=current_user.username)
            .order_by(Vehicle.vehicleName)).scalars()
        
    except Exception as e:
        vehicles = "<p>The error:<br>" + str(e) + "</p>"
        
    return render_template('dashboard.html', form=form, vehicles=vehicles)

@app.route('/vehicle/<code>')
def vehicle(code):
    vehicles = db.session.execute(db.select(Vehicle)
        .filter_by(code=code)).scalars()
    for vehicle in vehicles:
        vehicleName = vehicle.vehicleName
        speedLimit = str(vehicle.speedLimit)
        
    with open("D:/1.VGU/CSE2023/SpeedTracker/templates") as myfile:
        textlst = myfile.read().split()
        x = np.array([textlst])
        y = x.astype(float)
        speedArray = []
        for speed in y:
            for i in range(len(speed)):
                speedArray.append(speed[i])
 
    return render_template('vehicle.html',vehicleName=vehicleName,speedLimit=speedLimit,speedArray=speedArray)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)