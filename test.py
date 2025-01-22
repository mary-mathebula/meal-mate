from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import random
import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'http//127.0.01:5000'  # Update your URI here
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Your models and routes follow here

if __name__ == "__main__":
    app.run(debug=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    db.drop_all()  # Drop all tables
    db.create_all()  # Create the tables again with the correct schema

    def __repr__(self):
        return f'<User {self.username}>'

# Define the RegistrationForm
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# Define the LoginForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Define the Spoonacular API URL and key
API_URL = "https://api.spoonacular.com/recipes/complexSearch"
API_KEY = "2ea52454f1b847d18e6190a5a4da19b1"  # Replace with your Spoonacular API Key

condition_mapping = {
    "low blood": "low-sugar",        # Example: You might want a low-sugar diet for low blood
    "ulcers": "gluten-free",         # Example: Ulcers may benefit from a gluten-free diet
    "low blood - vegetarian": "vegetarian",
    "ulcers - gluten-free": "gluten-free",
    "low blood - snack": "low-sugar",
    "ulcers - mild": "mild"
}

def fetch_meal_recommendations(condition, meal_time, allergies):
    # Map condition to a valid Spoonacular diet type
    diet_type = condition_mapping.get(condition.lower(), "")
    
    # Debugging: log the diet type
    print(f"Fetching meals with diet: {diet_type}, meal time: {meal_time}, allergies: {','.join(allergies)}")

    query_params = {
        "apiKey": API_KEY,
        "diet": diet_type,       # Using diet type based on the condition
        "type": meal_time,       # breakfast, lunch, or dinner
        "intolerances": ','.join(allergies), # Include allergies in the query
        "number": 20             # You can adjust this number based on how many meals you want
    }

    try:
        response = requests.get(API_URL, params=query_params)
        response.raise_for_status()
        meals = response.json().get('results', [])
        
        # If no meals are returned, log this and handle gracefully
        if not meals:
            print(f"No meals found for {condition} and {meal_time}.")
        
        return meals

    except requests.exceptions.RequestException as e:
        print(f"Error fetching meals: {e}")
        return []

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('register'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Hash the password before saving it to the database
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')

        # Create a new User object with the form data
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Set the user_id in session after registration
        session['user_id'] = new_user.id

        # Redirect to the main page after successful registration
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            return redirect(url_for('index'))

        # If login fails, display an error
        return "Login Failed. Check your credentials."

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    condition = request.json.get('condition')
    meal_time = request.json.get('meal_time')
    allergies = request.json.get('allergies', [])

    if not condition or not meal_time:
        return jsonify({'recommendation': 'Invalid input. Please select both a condition and meal time.'})

    # Fetch meal recommendations from the API
    meals = fetch_meal_recommendations(condition, meal_time, allergies)
    
    if meals:
        # Randomly pick a meal to display
        recommendation = random.choice(meals)
        return jsonify({'recommendation': recommendation['title']})
    else:
        return jsonify({'recommendation': 'No recommendations available for this condition and meal time. Please try another combination.'})

if __name__ == "__main__":
    # Create database and tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)
