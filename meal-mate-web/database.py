# database.py
import sqlite3

# Create connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('user_profiles.db')  # This will create the database file if it doesn't exist
    return conn

# Create the user_profile table if it doesn't already exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            health_condition TEXT NOT NULL
        )
    ''')

    conn.commit()  # Commit the changes
    conn.close()

# Save the user's profile data into the database
def save_profile(name, age, health_condition):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO user_profile (name, age, health_condition)
        VALUES (?, ?, ?)
    ''', (name, age, health_condition))

    conn.commit()  # Save the changes
    conn.close()

# Load the most recent profile from the database
def load_profile():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()  # Fetch the latest profile

    conn.close()
    return result  # Return the profile data (None if no profile exists)
