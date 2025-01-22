from flask import Flask, render_template, request, jsonify
import requests
import random

app = Flask(__name__)

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
    return render_template('index.html')

@app.route('/', methods=['POST'])
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
    app.run(debug=True)
