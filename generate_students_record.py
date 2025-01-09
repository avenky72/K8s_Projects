#!/usr/bin/env python3

import mysql.connector
from faker import Faker
import random
import sys

# Use this to create the databases and table(s) needed
def run_query(query):
    #print("Run Query: {}".format(query))
    try:
       db_connection = mysql.connector.connect( host="127.0.0.1",  user="root",  password="mysql")
       cursor = db_connection.cursor()
       cursor.execute(query)
       connection.commit()
       cursor.close()
       db_connection.close()
    except Exception as e:
       print(e)
    return

# Function to generate random student data with unique student ID
def generate_student_data(student_id):
    name = fake.name()
    math = random.randint(50, 100)
    english = random.randint(50, 100)
    physics = random.randint(50, 100)
    chemistry = random.randint(50, 100)
    spanish = random.randint(50, 100)
    # Return the student data as a tuple, including the unique student ID
    return (name, student_id, math, english, physics, chemistry, spanish)

# Batch insert students into the database
def batch_insert_students(cursor, batch_size=1000, total_records=1000000):
    insert_query = """
    INSERT INTO students (name, student_id, math, english, physics, chemistry, spanish)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    # Initial student ID to start from
    student_id_counter = 100000
    
    # Loop to generate and insert records in batches
    for _ in range(total_records // batch_size):
        batch_data = []
        
        for _ in range(batch_size):
            # Create unique student ID and generate student data
            batch_data.append(generate_student_data(student_id_counter))
            student_id_counter += 1  # Increment student ID for the next student
        
        cursor.executemany(insert_query, batch_data)
        db_connection.commit()
        print(f"Inserted {batch_size} records")


### MAIN PROGRAM ####
        
if __name__ == '__main__':

    #db_create_query="CREATE DATABASE school; USE school; CREATE TABLE students ( id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), student_id INT UNIQUE, math INT, english INT, physics INT, chemistry INT, spanish INT )"
    db_create_query="CREATE DATABASE school; USE school; CREATE TABLE students (name VARCHAR(255), student_id INT UNIQUE, math INT, english INT, physics INT, chemistry INT, spanish INT )"

    # Initialize Faker to generate fake names
    fake = Faker()

    if len(sys.argv) < 2:
        print("Error: Missing Records count")
        sys.exit()

    max_records = int(sys.argv[1])
    
    # Setup database and table needed
    run_query(db_create_query)

    # Setup MySQL connection
    db_connection = mysql.connector.connect( host="127.0.0.1",  user="root",  password="mysql",  database="school")
    cursor = db_connection.cursor()

    # Run the batch insert for 100,000 students
    batch_insert_students(cursor, batch_size=5000, total_records=max_records)

    # Close the database connection
    cursor.close()
    db_connection.close()
    print("Data insertion complete!")

