from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

meal_recommendations = {
    "low blood": {
        "breakfast": [
            "Oatmeal with banana and almond butter.",
            "Whole grain toast with scrambled eggs and avocado.",
            "Greek yogurt with mixed berries and walnuts."
        ],
        "lunch": [
            "Grilled chicken salad with spinach, quinoa, and pumpkin seeds.",
            "Beef stir-fry with broccoli and brown rice.",
            "Lentil soup with a side of whole-grain bread."
        ],
        "dinner": [
            "Grilled steak with roasted sweet potatoes and green beans.",
            "Chicken curry with lentils and brown rice.",
            "Baked salmon with steamed broccoli and quinoa."
        ]
    },
    "ulcers": {
        "breakfast": [
            "Oatmeal with honey and a banana, paired with chamomile tea.",
            "Boiled eggs with a slice of whole wheat toast.",
            "Rice porridge with a bit of cinnamon and apple slices."
        ],
        "lunch": [
            "Grilled chicken with mashed potatoes and steamed zucchini.",
            "Baked fish with mashed sweet potatoes and boiled carrots.",
            "Toasted sandwich with mild cheese and cucumber."
        ],
        "dinner": [
            "Chicken breast with a side of boiled rice and carrots.",
            "Grilled turkey with roasted butternut squash and green beans.",
            "Steamed cod with mashed cauliflower and green peas."
        ]
    },
    "low blood - vegetarian": {
        "breakfast": [
            "Spinach smoothie with almond milk and a side of toast.",
            "Chia pudding with fresh berries and honey.",
            "Avocado toast topped with hemp seeds and lemon."
        ],
        "lunch": [
            "Lentil salad with roasted vegetables and arugula.",
            "Vegetable curry with brown rice.",
            "Stuffed bell peppers with quinoa and chickpeas."
        ],
        "dinner": [
            "Vegetable stir-fry with tofu and soba noodles.",
            "Grilled eggplant with tahini sauce and a side of couscous.",
            "Minestrone soup with a slice of whole-grain bread."
        ]
    },
    "ulcers - gluten-free": {
        "breakfast": [
            "Rice porridge with boiled apples and honey.",
            "Smoothie bowl with blended papaya, banana, and coconut flakes.",
            "Eggs with mashed avocado and gluten-free toast."
        ],
        "lunch": [
            "Grilled chicken with mashed cauliflower and steamed carrots.",
            "Baked salmon with roasted sweet potatoes and zucchini.",
            "Turkey lettuce wraps with cucumber and hummus."
        ],
        "dinner": [
            "Herb-roasted chicken with mashed pumpkin and green beans.",
            "Grilled cod with a side of quinoa and sautéed spinach.",
            "Beef stew with gluten-free dumplings and steamed broccoli."
        ]
    },
    "low blood - snack": {
        "breakfast": [
            "A boiled egg with a slice of avocado and a small handful of walnuts.",
            "Apple slices with peanut butter.",
            "Trail mix with dried fruits and nuts."
        ],
        "lunch": [
            "Smoothie made with spinach, banana, and orange juice.",
            "Hummus with carrot and cucumber sticks.",
            "Hard-boiled eggs with cherry tomatoes and a sprinkle of salt."
        ],
        "dinner": [
            "Yogurt parfait with granola and honey.",
            "Cheese cubes with grapes and whole-grain crackers.",
            "Pumpkin seeds with a glass of fortified plant-based milk."
        ]
    },
    "ulcers - mild": {
        "breakfast": [
            "Plain yogurt with soft, ripe bananas and a drizzle of honey.",
            "Rice pudding made with almond milk and cinnamon.",
            "Mashed avocado on soft toast with a sprinkle of salt."
        ],
        "lunch": [
            "Chicken soup with soft vegetables like carrots and potatoes.",
            "Steamed pumpkin with boiled chicken breast.",
            "Grilled turkey with a side of mashed squash."
        ],
        "dinner": [
            "Baked fish with soft sweet potato mash.",
            "Rice and steamed carrots with a drizzle of olive oil.",
            "Poached chicken with mashed cauliflower and boiled zucchini."
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html', recommendation=None)

@app.route('/', methods=['POST'])
def get_recommendation():
    condition = request.json.get('condition')
    meal_time = request.json.get('meal_time')

    # Log received data for debugging
    print(f"Received condition: {condition}, meal_time: {meal_time}")

    if not condition or not meal_time:
        return jsonify({'recommendation': 'Invalid input. Please select both a condition and meal time.'})

    # Get recommendations based on condition and meal time
    recommendations = meal_recommendations.get(condition.lower(), {}).get(meal_time.lower(), [])

    # Log recommendations for debugging
    print(f"Found recommendations: {recommendations}")

    if recommendations:
        recommendation = random.choice(recommendations)
        return jsonify({'recommendation': recommendation})
    else:
        return jsonify({'recommendation': 'No recommendations available for this condition and meal time. Please try another combination.'})

if __name__ == "__main__":
    app.run(debug=True)