import sqlite3
import json

# Your data
dog_data = {
    'name': 'Dog',
    'age': 7,
    'is_employee': False,
    'vector': [1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 7.8],  # A list of floats
    'matched_result_id': ['Cat#cat@gmail', 'Dog#dog@gmail'],  # A list of strings
}

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('pets.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS dogs (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    is_employee BOOLEAN,
    vector TEXT,
    matched_result_id TEXT
)
''')

# Serialize list and dict data to JSON for storage
dog_data['vector'] = json.dumps(dog_data['vector'])
dog_data['matched_result_id'] = json.dumps(dog_data['matched_result_id'])

# Insert data into table
cursor.execute('''
INSERT INTO dogs (name, age, is_employee, vector, matched_result_id)
VALUES (:name, :age, :is_employee, :vector, :matched_result_id)
''', dog_data)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()