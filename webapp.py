from flask import Flask, request, jsonify
import mysql.connector
import random
import os
import json
import logging

# Initialize Flask app
app = Flask(__name__)

portnum = 5000
db_connected = 0
cursor = {}

# DB
db_name = "school"


# MySQL connection setup
mysql_host = os.getenv("MYSQL_HOST", '127.0.0.1')
mysql_user = os.getenv("MYSQL_USER", 'root')
mysql_passwd = os.getenv("MYSQL_PASSWORD", 'mysql')
mysql_port = os.getenv("MYSQL_PORT", '3306')

db_connection = None

##
## Function to Connect to DB
##
def db_connect():
   global db_connected
   global cursor
   global db_connection
   print("INFO: Connecting to DB")
   try:
      db_connection = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_passwd, database=db_name)
      db_connected = 1
   except Exception as e:
      print("ERROR: MySQL DB connection failed")
      print(e)
   logging.info('Connected to MySQL Database')
   return db_connection

# Establish DB connection
db_connection = db_connect()

logging.basicConfig(level=logging.DEBUG)


##
## Route to run a custom SQL query directly
##
@app.route('/api/run_query', methods=['POST'])
def run_query():
    global db_connected
    global db_connection
    global cursor

    try:
       query = request.json.get('query')
       query = query.lower()
       print("QUERY: {}".format(query))
       logging.info("QUERY: Received: ", query)
    except Exception as e:
       return jsonify({'error': 'No query provided'}), 400

    if query:
        try:
            # Execute the query
            cursor = db_connection.cursor(dictionary=True)
            cursor.execute(query)
            # If it's a SELECT query, fetch the results
            if query.startswith("select"):
                result = cursor.fetchall()
                #rows = cursor.fetchall()
                #result = [dict(row) for row in rows]  # Convert rows to dictionary
                return jsonify(result), 200
            else:
                # Commit the transaction for non-SELECT queries
                logging.info('DB: Committed')
                db_connection.commit()
                return jsonify({'message': 'Query executed successfully!'}), 200
        except Exception as e:
            db_connection = db_connect()
            return jsonify({'DB error': str(e)}), 400


##
## API Call to get n random students data
##
@app.route('/api/get_students', methods=['GET'])
def get_students():
    global db_connected
    global db_connection
    global cursor

    query = "select * from students;"

    # Get 'n' parameter from the request URL
    try:
        n = int(request.args.get('n', 10))  # Default 10 records 
    except ValueError:
        return jsonify({"error": "'n' must be an integer"}), 400

    # check 'n' is not negative
    if n <= 0:
        return jsonify({"error": "'n' must be a positive integer"}), 400

    try:
       # Query the database to get few 100s of students ONLY
       cursor = db_connection.cursor(dictionary=True)
       cursor.execute(query)
       all_students = cursor.fetchall()

       # If there are fewer students than requested, return all students
       #print("Fetch {} students".format(n))
       if len(all_students) < n:
           return jsonify(all_students)

       # Randomly select 'n' student records
       random_students = random.sample(all_students, n)
       # Return data
       return jsonify(random_students)
    except Exception as e:
       db_connection = db_connect()
       #print({"ERROR: {}".format(e)})
       return jsonify({'DB error': str(e)}), 400

##
## Count the number of student records
##
@app.route('/api/students/count', methods=['GET'])
def user_count():
    global db_connected
    global db_connection
    global cursor

    try:
       query = "SELECT COUNT(*) FROM students;"
       cursor = db_connection.cursor(dictionary=True)
       cursor.execute(query)
       count = cursor.fetchall()
       return jsonify({"user_count": count}), 200
    except Exception as e:
       db_connection = db_connect()
       return jsonify({"ERROR: {}".format(e)}), 404


##
## Delete a student record using id - Approach 2 - WORKS
##
@app.route('/api/delete_id', methods=['DELETE'])
def delete_student():
    global db_connected
    global db_connection
    global cursor

    try:
       id = request.json.get('id')
       query = "delete from students where student_id={};".format(id)
       cursor = db_connection.cursor(dictionary=True)
       cursor.execute(query)
       db_connection.commit()  # Run commit to make the change final
       return jsonify({"Deleted student id": id}), 200
    except Exception as e:
       db_connection = db_connect()
       return jsonify({"ERROR: {}".format(e)}), 404
    else:
       return jsonify({"error": "Student not found"}), 404


if __name__ == '__main__':
    app.run(port=portnum, debug=True)

