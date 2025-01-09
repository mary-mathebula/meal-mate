from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import json
import sqlite3
import os

# Initialize Flask app
app = Flask(__name__)

# Database setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meal_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the UserProfile model
class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_condition = db.Column(db.String(150), nullable=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Background task to send food recommendations
def send_daily_recommendation():
    print("Sending daily food recommendation...")

# Set up the scheduler for daily reminders
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_daily_recommendation, trigger="interval", hours=24)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        health_condition = request.form['health_condition']

        new_profile = UserProfile(name=name, age=age, health_condition=health_condition)
        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for('profile', profile_id=new_profile.id))

    return render_template('create_profile.html')

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    profile = UserProfile.query.get_or_404(profile_id)
    return render_template('profile.html', profile=profile)


@app.route('/recommendations')
def recommendations():
    try:
        # Try to open the meals.json file
        with open('meals.json') as f:
            meals = json.load(f)
        
        # If successful, render the recommendations page with the meals
        return render_template('recommendations.html', meals=meals)

    except FileNotFoundError:
        # If the file is not found, return an error message
        return "The meals.json file is missing. Please check your setup."

    except json.JSONDecodeError:
        # In case the file exists but is not valid JSON, handle that error
        return "The meals.json file exists but contains invalid JSON."




if __name__ == '__main__':
    app.run(debug=True)
