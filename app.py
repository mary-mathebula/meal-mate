import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from plyer import notification
import time
import threading
import sqlite3
import datetime
import json

# SQLite Database setup
def create_connection():
    conn = sqlite3.connect("meal_mate.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile
                    (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, health_condition TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS meal_log
                    (id INTEGER PRIMARY KEY, user_id INTEGER, meal_name TEXT, meal_time TEXT, meal_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES user_profile (id))''')
    conn.commit()

# Function to save the profile to SQLite DB
def save_profile():
    name = name_entry.get()
    age = age_entry.get()
    health_condition = health_condition_entry.get()

    # Check if all fields are filled
    if name == "" or age == "" or health_condition == "":
        messagebox.showerror("Input Error", "Please fill out all fields.")
        return

    # Connect to the database and insert the user profile
    conn = create_connection()
    cursor = conn.cursor()

    # Insert the user's profile into the database
    cursor.execute("INSERT INTO user_profile (name, age, health_condition) VALUES (?, ?, ?)", 
                   (name, age, health_condition))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Confirm that the profile is saved
    messagebox.showinfo("Profile Saved", "Your profile has been saved!")


# Function to load profile from SQLite DB
def load_profile():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        print(f"Loaded profile: Name: {result[1]}, Age: {result[2]}, Health Condition: {result[3]}")  # Debugging
        name_entry.insert(0, result[1])
        age_entry.insert(0, result[2])
        health_condition_entry.insert(0, result[3])
    else:
        messagebox.showinfo("No Profile Found", "No user profile found. Please create one.")

    conn.close()


# Function to get meal recommendations based on health condition
def get_meal_recommendation(health_condition):
    if health_condition.lower() == "low iron":
        return ["Spinach", "Liver", "Lentils", "Red Meat"]
    elif health_condition.lower() == "vegetarian":
        return ["Tofu", "Quinoa", "Spinach", "Chickpeas"]
    elif health_condition.lower() == "vegan":
        return ["Tofu", "Lentils", "Oats", "Soy Milk"]
    else:
        return ["Chicken", "Rice", "Vegetables", "Salad"]

# Function to show meal recommendations
def show_recommendations():
    health_condition = health_condition_entry.get()
    recommendations = get_meal_recommendation(health_condition)
    recommendation_label.config(text=f"Meal Recommendations: {', '.join(recommendations)}")

# Function to check if it's time for a meal
def check_time_for_meal(meal_time):
    current_time = datetime.datetime.now().strftime("%H:%M")
    return current_time == meal_time

# Function to send custom meal reminders
def send_custom_meal_reminders():
    while True:
        breakfast_time = breakfast_time_entry.get()
        lunch_time = lunch_time_entry.get()
        dinner_time = dinner_time_entry.get()
        
        if check_time_for_meal(breakfast_time):
            notification.notify(
                title="Meal Reminder",
                message="It's time for Breakfast!",
                timeout=10
            )
        if check_time_for_meal(lunch_time):
            notification.notify(
                title="Meal Reminder",
                message="It's time for Lunch!",
                timeout=10
            )
        if check_time_for_meal(dinner_time):
            notification.notify(
                title="Meal Reminder",
                message="It's time for Dinner!",
                timeout=10
            )
        
        time.sleep(60)  # Check every minute

# To make reminders work continuously, run them in a separate thread
def start_reminders():
    reminder_thread = threading.Thread(target=send_custom_meal_reminders)
    reminder_thread.daemon = True  # Allow the thread to exit when the main app exits
    reminder_thread.start()

# Function to log the meal eaten by the user
def log_meal(meal_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user_profile ORDER BY id DESC LIMIT 1")
    user_id = cursor.fetchone()[0]
    
    meal_time = datetime.datetime.now().strftime("%H:%M")
    meal_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO meal_log (user_id, meal_name, meal_time, meal_date) VALUES (?, ?, ?, ?)",
                   (user_id, meal_name, meal_time, meal_date))
    conn.commit()

    messagebox.showinfo("Meal Logged", f"Meal '{meal_name}' has been logged for {meal_date} at {meal_time}.")

    # Function to set up database tables
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    # Create user_profile table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile
                    (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, health_condition TEXT)''')
    # Create meal_log table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS meal_log
                    (id INTEGER PRIMARY KEY, user_id INTEGER, meal_name TEXT, meal_time TEXT, meal_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES user_profile (id))''')
    conn.commit()
    conn.close()

# Call the create_tables function at the start of the app to ensure the database is ready
create_tables()

# Function to load profile from SQLite DB
def load_profile():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()

    if result:
        name_entry.insert(0, result[1])
        age_entry.insert(0, result[2])
        health_condition_entry.insert(0, result[3])

# The rest of the code follows as before...


# Set up Tkinter window
root = tk.Tk()
root.title("Meal Mate")

# Add labels and entry fields for profile form
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Age:").grid(row=1, column=0, padx=5, pady=5)
age_entry = ttk.Entry(root)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Health Condition (e.g., Low Iron):").grid(row=2, column=0, padx=5, pady=5)
health_condition_entry = ttk.Entry(root)
health_condition_entry.grid(row=2, column=1, padx=5, pady=5)

# Save profile button
save_button = ttk.Button(root, text="Save Profile", command=save_profile)
save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Meal recommendations section
recommend_button = ttk.Button(root, text="Get Meal Recommendations", command=show_recommendations)
recommend_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Label to display meal recommendations
recommendation_label = ttk.Label(root, text="Meal Recommendations: ")
recommendation_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Add labels and entry fields for custom reminder times
tk.Label(root, text="Breakfast Time (HH:MM):").grid(row=6, column=0, padx=5, pady=5)
breakfast_time_entry = ttk.Entry(root)
breakfast_time_entry.grid(row=6, column=1, padx=5, pady=5)

tk.Label(root, text="Lunch Time (HH:MM):").grid(row=7, column=0, padx=5, pady=5)
lunch_time_entry = ttk.Entry(root)
lunch_time_entry.grid(row=7, column=1, padx=5, pady=5)

tk.Label(root, text="Dinner Time (HH:MM):").grid(row=8, column=0, padx=5, pady=5)
dinner_time_entry = ttk.Entry(root)
dinner_time_entry.grid(row=8, column=1, padx=5, pady=5)

# Button to start meal reminders
reminder_button = ttk.Button(root, text="Start Meal Reminders", command=start_reminders)
reminder_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Meal logging
log_meal_button = ttk.Button(root, text="Log Meal", command=lambda: log_meal('Breakfast'))
log_meal_button.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Load profile data when the app starts
load_profile()

# Initialize the database
create_tables()

root.mainloop()
