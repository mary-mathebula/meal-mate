from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import json
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

        # Check if the profile already exists
        existing_profile = UserProfile.query.filter_by(name=name).first()
        if existing_profile:
            # Redirect to the existing profile or show a message
            return redirect(url_for('profile', profile_id=existing_profile.id))

        # If the profile doesn't exist, create a new one
        new_profile = UserProfile(name=name, age=age, health_condition=health_condition)
        db.session.add(new_profile)
        db.session.commit()

        return redirect(url_for('profile', profile_id=new_profile.id))

    return render_template('create_profile.html')

@app.route('/profile/<int:profile_id>')
def profile(profile_id):
    profile = UserProfile.query.get_or_404(profile_id)
    return render_template('profile.html', profile=profile)

@app.route('/profiles')
def profiles():
    # Get all profiles from the database
    all_profiles = UserProfile.query.all()
    return render_template('profiles.html', profiles=all_profiles)



@app.route('/recommendations')
def recommendations():
    try:
        # Open meals.json file
        
        with open(os.path.join(app.root_path, 'static', 'meals.json')) as f:
            meals = json.load(f)

        # Get the user's preferred diet, category, or high iron filter
        diet_filter = request.args.get('diet', '')
        category_filter = request.args.get('category', '')
        high_iron_filter = request.args.get('high_iron', '')

        # Filter meals based on the diet preference
        if diet_filter:
            meals = [meal for meal in meals if diet_filter.lower() in meal['diet'].lower()]

        # Filter meals based on the category preference
        if category_filter:
            meals = [meal for meal in meals if category_filter.lower() in meal['category'].lower()]

        # Filter meals based on the high iron preference (new filter)
        if high_iron_filter.lower() == 'true':
            meals = [meal for meal in meals if meal.get('high_iron', False)]

        return render_template('recommendations.html', meals=meals)

    except FileNotFoundError:
        return "The meals.json file is missing. Please check your setup."

    except json.JSONDecodeError:
        return "The meals.json file exists but contains invalid JSON."
    


UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return 'No file part'
    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'File uploaded successfully'



if __name__ == '__main__':
    app.run(debug=True)
