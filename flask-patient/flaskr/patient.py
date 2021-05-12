from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
from datetime import datetime
from pytz import timezone

pt = Blueprint('patient', __name__)
tz = timezone('EST')

@pt.route('/patient/patient/today/<rmId>', methods=['GET'])
def today(rmId):
	print(rmId);
	db = get_db()
	today = datetime.now(tz)
	#today = "2021-03-24"
	db.execute("SELECT DATEPART(hour, CAST(L.time_of_day AS TIME)), sum(L.distance), avg(L.speed), sum(L.duration), sum(L.ambulation) FROM mmambulation.live_details AS L, mmambulation.patient_info AS P WHERE L.patient_id = P.patient_id AND L.date = %s AND P.room_number = %s GROUP BY DATEPART(hour, CAST(L.time_of_day AS TIME));", (today, rmId))
	result= db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp

@pt.route('/patient/patient/week/<rmId>', methods=['GET'])
def week(rmId):
	db = get_db()
	#today = datetime.now(tz)
	today = "2021-03-24"
	db.execute("SELECT DATEPART(dw, L.date), sum(L.distance), avg(L.speed), sum(L.duration), sum(L.ambulation) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE P.room_number = %s AND L.date >=  (DATEADD(dd, -(DATEPART(dw, %s)-1), %s)) GROUP BY CAST(L.date as DATE);", (rmId, today, today))
	result = db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp

@pt.route('/patient/patient/month/<rmId>', methods=['GET'])
def month(rmId):
	db = get_db()
	#today = datetime.now(tz)
	today = "2021-03-24"
	db.execute("SELECT DATEPART(d, L.date), sum(L.distance), avg(L.speed), sum(L.duration), sum(L.ambulation) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE P.room_number = %s AND L.date >=  (DATEADD(dd, -(DATEPART(dd, %s)-1), %s)) GROUP BY CAST(L.date as DATE);", (rmId, today, today))
	result = db.fetchall()
	x = []
	for row in result:
		x.append({"date": row[0], "distance": row[1], "speed": row[2], "duration": row[3], "num_amb": row[4]})
	resp = jsonify(x)
	return resp