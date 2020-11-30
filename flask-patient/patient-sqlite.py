from flask import Flask, request, jsonify
import json
import sqlite3

def init_db():
    conn = sqlite3.connect('pmr.db')
    cursor = conn.cursor()
    with open('schema.sql') as f:
        cursor.executescript(f.read())
    return

def patient_today(patient_id, date):
    patient = {}
    patient['type'] = 'today'

    conn = sqlite3.connect('pmr.db')
    cursor = conn.cursor()

    sql = ("SELECT sum(distance) as distance, sum(duration) as duration,\
        count(ambulation) as ambulation\
            FROM live_details WHERE (patient_ID = ? and date = ? )")
    data = (patient_id, date)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    name = [column[0] for column in cursor.description]
    patient = {}
    for index in range(len(name)):
        patient[name[index]] = result[index]

    try:
        if patient['distance'] is None or patient['duration'] is None:
            patient['result'] = 'None'
        else:
            patient['result'] = 'valid'
    except KeyError:
        patient['result'] = 'None'
    conn.close()
    return json.dumps(patient)

def patient_login(username, password):
    conn = sqlite3.connect('pmr.db')
    cursor = conn.cursor()
    sql = ("SELECT password FROM patient_info WHERE username = ?")
    data = (username,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    valid = False

    if result[0] == password:
        valid = True

    patient = {}

    if valid:
        patient['valid'] = True
        
        # If user can log in to server, get other information as well
        # Get patient ID from the SQL
        sql = "SELECT patient_ID FROM patient_info WHERE username = ?"
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.fetchone()
        if result[0] != None:
            patient['id'] = result[0]
        else:
            patient['id'] = "None"

        # Get room number from the SQL
        sql = "SELECT room_number FROM patient_info WHERE username = ?"
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

def patient_all(patient_id):
    conn = sqlite3.connect('pmr.db')
    cursor = conn.cursor()
    
    patient = {}
    start_date = None

    sql = ("SELECT transfer_date as start_datetime FROM patient_info\
         WHERE patient_ID = ?")
    data = (patient_id,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    if result == None:
        patient['result'] = "None"
    else: 
        start_date = result[0]

    patient['start'] = start_date
    patient['type'] = 'all'

    sql = ("SELECT sum(distance) as distance, sum(duration) as duration, \
        count(ambulation) as ambulation, max(date) as end \
            FROM live_details WHERE (patient_ID = ?)")
    data = (patient_id,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    name = [column[0] for column in cursor.description]
    for index in range(len(name)):
        patient[name[index]] = result[index]
    
    try:
        if patient['distance'] is None or patient['duration'] is None:
            patient['result'] = "None"
        else:
            patient['result'] = "valid"
    except KeyError:
        patient['result'] = "None"
    conn.close()
    return json.dumps(patient)

def patient_graph(patient_id, table_type):
    conn = sqlite3.connect('pmr.db')
    cursor = conn.cursor()
    
    patient = {}
    start_date = None

    sql = ("SELECT transfer_date as start_datetime FROM patient_info\
         WHERE patient_ID = ?")
    data = (patient_id,)
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchone()
    if result == None:
        patient['result'] = "None"
    else: 
        start_date = result[0]

    sql = ""
    if table_type == 'ambulation':
        sql = "SELECT date, count(ambulation) as result FROM live_details \
            WHERE (patient_id = ? and date >= ?) GROUP BY date"
    elif table_type == 'distance':
        sql = "SELECT date, sum(distance) as result FROM live_details \
            WHERE (patient_id = ? and date >= ?) GROUP BY date"
    else:
        # type is 'speed'
        sql = "SELECT date, sum(distance)/sum(duration) as result FROM live_details \
            WHERE (patient_id = ? and date >= ?) GROUP BY date"
    data = (patient_id, start_date)

    values = []
    cursor.execute(sql, data)
    conn.commit()
    result = cursor.fetchall()
    name = [column[0] for column in cursor.description]
    for row in result:
        value = dict()
        for index in range(len(name)):
            value[name[index]] = row[index]
        values.append(value)
    return json.dumps(values)

# Mainly for testing purposes
if __name__ == "__main__":
    # Create a sample SQLite table
    # init_db()
    print(patient_today(500, '2019-05-01'))
    print(patient_today(501, '2019-05-02'))
    print(patient_login('username', 'password'))
    print(patient_login('admin', '123'))
    print(patient_all(500))
    print(patient_all(501))
    print(patient_graph(500, 'distance'))
    print(patient_graph(500, 'speed'))
    print(patient_graph(501, 'distance'))