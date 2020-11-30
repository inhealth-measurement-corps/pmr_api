from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
from datetime import date

pt = Blueprint('patient', __name__)

@pt.route('/clinician/patient/today/<rmId>', methods=['GET'])
def today(rmId):
	print(rmId);
	db = get_db()
	today = "2020-03-12"
	# today = date.today()
	db.execute("SELECT DATEPART(hour, CAST(L.time_of_day AS TIME)), sum(L.distance), (sum(L.distance)/sum(L.duration))*0.0113636*60, sum(L.duration), count(L.time_of_day) FROM mmambulation.live_details AS L, mmambulation.patient_info AS P WHERE L.patient_id = P.patient_id AND L.date = %s AND P.room_number = %s GROUP BY DATEPART(hour, CAST(L.time_of_day AS TIME));", (today, rmId))                   
	result= db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp

@pt.route('/clinician/patient/week/<rmId>', methods=['GET'])
def week(rmId):
	db = get_db()
	today = date.today()
	db.execute("SELECT DATEPART(dw, L.ambulation), sum(L.distance), (sum(L.distance)/sum(L.duration))*0.0113636*60, sum(L.duration), count(L.time_of_day) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE P.room_number = %s AND L.ambulation >=  (DATEADD(dd, -(DATEPART(dw, %s)-1), %s)) GROUP BY CAST(L.ambulation as DATE);", (rmId, today, today))
	result = db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp

@pt.route('/clinician/patient/month/<rmId>', methods=['GET'])
def month(rmId):
	db = get_db()
	today = date.today()
	db.execute("SELECT DATEPART(d, L.ambulation), sum(L.distance), (sum(L.distance)/sum(L.duration))*0.0113636*60, sum(L.duration), count(L.time_of_day) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE P.room_number = %s AND L.ambulation >=  (DATEADD(dd, -(DATEPART(dd, %s)-1), %s)) GROUP BY CAST(L.ambulation as DATE);", (rmId, today, today))
	result = db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp