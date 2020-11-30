from flask import Flask, request, jsonify
import json

from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()

# MySQL Configuration
# TODO: NEED TO CHECK WHEN POST ON THE NEW SERVER
app.config['MYSQL_DATABASE_HOST'] = 'ESMPMMCADBDEV1.win.ad.jhu.edu'
app.config['MYSQL_DATABASE_USER'] = 'pmr'
app.config['MYSQL_DATABASE_PASSWORD'] = 'kQSSD0J9gY4h2hj5OIPp'
app.config['MYSQL_DATABASE_DB'] = 'pmr'
mysql.init_app(app)

'''
Default return
'''
@app.route("/")
def hello():
    return "Hello World"

'''
Get today's data for patient of certain patient_id
'''
@app.route("/patient/today", methods=['GET'])
def patient_today():
    # Get parameters from front-end
    param = request.get_json()
    patient_id = param['patient_id']
    date = param['date']

    # Initialize result
    patient = {}
    patient['type'] = 'today'

    # Connect to the server
    conn = mysql.connect()
    cursor = conn.cursor()

    # Query today's data for patients
    sql = ("SELECT sum(distance) as distance, sum(duration) as duration,\
        count(ambulation) as ambulation\
            FROM live_details WHERE (patient_ID = %s and date = %s )")
    data = (patient_id, date)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    name = [column[0] for column in cursor.description]
    
    # Assign values
    for index in range(len(name)):
        patient[name[index]] = result[index]

    # Check for invalid cases
    try:
        if patient['distance'] is None or patient['duration'] is None:
            patient['result'] = 'None'
        else:
            patient['result'] = 'valid'
    except KeyError:
        patient['result'] = 'None'
    conn.close()
    return json.dumps(patient)

'''
Verify if user is logging in correctly
'''
@app.route("/patient/login", methods=['GET'])
def patient_login():
    # Parameters from front end
    param = request.get_json()
    username = param['username']
    password = param['password']

    # Connect to the server
    conn = mysql.connect()
    cursor = conn.cursor()

    # Query to get the password
    sql = ("SELECT password FROM patient_info WHERE username = %s")
    data = (username,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()

    # Verify password
    valid = False
    if result[0] == password:
        valid = True

    # If user can login, query other information
    patient = {}
    if valid:
        patient['valid'] = True
        
        # Get patient ID from the SQL
        sql = "SELECT patient_ID FROM patient_info WHERE username = %s"
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.fetchone()
        if result[0] != None:
            patient['id'] = result[0]
        else:
            patient['id'] = "None"

        # Get room number from the SQL
        sql = "SELECT room_number FROM patient_info WHERE username = %s"
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.fetchone()
        if result[0] != None:
            patient['room'] = result[0]
        else:
            patient['room'] = "None"
    else:
        patient['valid'] = False
    conn.close()
    return json.dumps(patient)

'''
Get all data for certain patient ID
'''
@app.route("/patient/all", methods=['GET'])
def patient_all():
    # Get the parameters from the front-end
    param = request.get_json()
    patient_id = param['patient_id']
    
    # Initialize the results
    patient = {}
    start_date = None

    # Connect to the database
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = ("SELECT transfer_date as start_datetime FROM patient_info WHERE patient_ID = %s")
    data = (patient_id,)
    cursor.execute(sql, data)
    conn.commit()

    # Get the start date
    result = cursor.fetchone()
    if result == None:
        patient['result'] = "None"
    else: 
        start_date = result[0]

    # For result purposes
    patient['start'] = start_date
    patient['type'] = 'all'
    
    # Get all information from the database
    sql = ("SELECT sum(distance) as distance, sum(duration) as duration, \
        count(ambulation) as ambulation, max(date) as end_datetime \
            FROM live_details WHERE (patient_ID = %s)")
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    name = [column[0] for column in cursor.description]
    for index in range(len(name)):
        patient[name[index]] = result[index]
    
    # Handle invalid cases
    try:
        if patient['distance'] is None or patient['duration'] is None:
            patient['result'] = "None"
        else:
            patient['result'] = "valid"
    except KeyError:
        patient['result'] = "None"
    conn.close()
    return json.dumps(patient)

'''
Get data to support graphing for patient's data
'''
@app.route("/patient/graph", methods=['GET'])
def patient_graph():
    # Get parameters from front-end
    param = request.get_json()
    patient_id = param['patient_id']
    table_type = param['type']
    
    start_date = None
    patient = {}

    # Connect to the database
    conn = mysql.connect()
    cursor = conn.cursor()

    # Get the transfer date as the start date
    sql = ("SELECT transfer_date as start_datetime FROM patient_info WHERE patient_ID = %s")
    data = (patient_id,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    if result == None:
        patient['result'] = "None"
    else: 
        start_date = result[0]

    # Get all the data based on the kind of graphs
    sql = ""
    if table_type == 'ambulation':
        sql = "SELECT date, count(ambulation) as result FROM live_details \
            WHERE (patient_id = %s and date >= %s) GROUP BY date"
    elif table_type == 'distance':
        sql = "SELECT date, sum(distance) as result FROM live_details \
            WHERE (patient_id = %s and date >= %s) GROUP BY date"
    else:
        # type is 'speed'
        sql = "SELECT date, sum(distance)/sum(duration) as result FROM live_details \
            WHERE (patient_id = %s and date >= %s) GROUP BY date"
    data = (patient_id, start_date)

    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchall()
    
    # Get all the values from the servers as a list
    name = [column[0] for column in cursor.description]
    values = []
    for row in result:
        value = dict()
        for index in range(len(name)):
            value[name[index]] = row[index]
        values.append(value)
    return json.dumps(values)