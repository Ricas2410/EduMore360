import os
import django
import sqlite3

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

# Get the database path from Django settings
from django.conf import settings
db_path = settings.DATABASES['default']['NAME']

print(f"Using database: {db_path}")

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read the SQL script
with open('sample_questions.sql', 'r') as f:
    sql_script = f.read()

# Split the script into individual statements
statements = sql_script.split(';')

# Variables to store IDs
noun_q1_id = None
noun_q2_id = None
noun_q3_id = None
noun_sa1_id = None
noun_sa2_id = None

# Execute each statement
for statement in statements:
    statement = statement.strip()
    if not statement:
        continue

    # Skip comments
    if statement.startswith('--'):
        continue

    try:
        # Check if this is an INSERT statement for a question
        if 'INSERT INTO quiz_question' in statement:
            # Execute the statement
            cursor.execute(statement)

            # Get the ID of the inserted question
            last_id = cursor.lastrowid
            print(f"Inserted question with ID: {last_id}")

            # Determine which question this is
            if 'Which of the following is a proper noun?' in statement:
                noun_q1_id = last_id
                print(f"noun_q1_id = {noun_q1_id}")
            elif 'Which sentence contains a collective noun?' in statement:
                noun_q2_id = last_id
                print(f"noun_q2_id = {noun_q2_id}")
            elif 'Which of the following is an abstract noun?' in statement:
                noun_q3_id = last_id
                print(f"noun_q3_id = {noun_q3_id}")
            elif 'Write a proper noun for a famous city.' in statement:
                noun_sa1_id = last_id
                print(f"noun_sa1_id = {noun_sa1_id}")
            elif 'What is a collective noun for a group of lions?' in statement:
                noun_sa2_id = last_id
                print(f"noun_sa2_id = {noun_sa2_id}")

        # Check if this is an INSERT statement for choices or answers
        elif 'INSERT INTO quiz_questionchoice' in statement or 'INSERT INTO quiz_shortanswer' in statement:
            # Replace variable placeholders with actual IDs
            if '@noun_q1_id' in statement:
                statement = statement.replace('@noun_q1_id', str(noun_q1_id))
            elif '@noun_q2_id' in statement:
                statement = statement.replace('@noun_q2_id', str(noun_q2_id))
            elif '@noun_q3_id' in statement:
                statement = statement.replace('@noun_q3_id', str(noun_q3_id))
            elif '@noun_sa1_id' in statement:
                statement = statement.replace('@noun_sa1_id', str(noun_sa1_id))
            elif '@noun_sa2_id' in statement:
                statement = statement.replace('@noun_sa2_id', str(noun_sa2_id))

            # Execute the modified statement
            cursor.execute(statement)
            print(f"Inserted choices/answers for question")

        # For all other statements
        else:
            cursor.execute(statement)
            print(f"Executed statement: {statement[:50]}...")

    except Exception as e:
        print(f"Error executing statement: {statement[:100]}...")
        print(f"Error: {e}")

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Sample questions added successfully!")
