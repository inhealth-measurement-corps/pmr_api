# -*- coding: utf-8 -*-
from flask import (
    Blueprint, jsonify, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
from datetime import date

ut = Blueprint('unit', __name__)


@ut.route('/clinician/unit/week', methods=['GET'])
def week():
	db = get_db()
	#today = date.today()
	today = "2020-12-02"
	db.execute("SELECT sum(L.distance)/count(distinct L.patient_ID), avg(L.speed), sum(L.duration)/count(distinct L.patient_ID), sum(L.ambulation)/count(distinct L.patient_ID) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE L.date >=  (DATEADD(dd, -(DATEPART(dw, %s)-1), %s));", (today, today))
	row = db.fetchone()
	x = [{"date": 0, "distance": row[0], "speed": row[1], "duration": row[2], "num_amb": row[3]}]
	resp = jsonify(x)
	return resp

@ut.route('/clinician/unit/month', methods=['GET'])
def month():
	db = get_db()
	today = date.today()
	db.execute("SELECT sum(L.distance)/count(distinct L.patient_ID), avg(L.speed), sum(L.duration)/count(distinct L.patient_ID), sum(L.ambulation)/count(distinct L.patient_ID) FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID WHERE L.date >=  (DATEADD(dd, -(DATEPART(dd, %s)-1), %s));", (today, today))
	row = db.fetchone()
	x = [{"date": 0, "distance": row[0], "speed": row[1], "duration": row[2], "num_amb": row[3]}]
	resp = jsonify(x)
	return resp

@ut.route('/clinician/unit/details', methods=['GET'])
def details():
	db = get_db()
	#today = date.today()
	today = "2020-11-30"
	query_total = 'SELECT L.patient_ID AS id , sum(L.distance) AS distance, sum(L.duration) AS duration, count(L.ambulation) AS ambulation, max(P.room_number) AS room, DATEDIFF(dd, max(P.admission_date), %s) AS total_los, DATEDIFF(dd, max(P.transfer_date), %s) AS pcu_los, count(L.ambulation)/DATEDIFF(dd, max(P.transfer_date), %s) AS avg_amb FROM mmambulation.live_details AS L LEFT JOIN mmambulation.patient_info AS P ON L.patient_ID = P.patient_ID GROUP BY L.patient_ID ORDER BY L.patient_ID'
	db.execute(query_total, (today, today, today))
	result_total = db.fetchall()
	query_today = 'SELECT patient_ID AS id, sum(distance) AS today_distance, sum(duration) AS today_duration, count(ambulation) AS today_ambulation FROM mmambulation.live_details WHERE date = %s GROUP BY patient_ID ORDER BY patient_ID'
	db.execute(query_today, (today))
	result_today = db.fetchall()
	query_yest = 'SELECT patient_ID AS id, sum(distance) AS yest_distance, sum(duration) AS yest_duration, count(ambulation) AS yest_ambulation FROM mmambulation.live_details WHERE date = DATEADD(dd, -1, %s) GROUP BY patient_ID ORDER BY patient_ID'
	db.execute(query_yest, (today))
	result_yest = db.fetchall()
	print(result_total)
	print("\n")
	print(result_yest)
	print("\n")
	print(result_today)
	x = []
	i = 0
	j = 0
	k = 0
	while(i < len(result_total)):
		row_total = result_total[i]
		id = row_total[0]
		# when patient id matches/patient has ambulation both today and yesterday
		if(j < len(result_today) and k < len(result_yest) and id == result_today[j][0] and id == result_yest[k][0]):
			row_today = result_today[j]
			row_yest = result_yest[k]
			x.append({"id": row_total[0], "total_dist": row_total[1], "total_dur": row_total[2], "total_amb": row_total[3], "room": row_total[4], "total_los": row_total[5], "pcu_los": row_total[6], "avg_amb": row_total[7], "today_dist": row_today[1], "today_dur": row_today[2], "today_amb": row_today[3], "yest_dist": row_yest[1], "yest_dur": row_yest[2], "yest_amb": row_yest[3]})
			i = i + 1
			j = j + 1
			k = k + 1
		elif(j < len(result_today) and id == result_today[j][0]): 
			# when a patient didn't have ambulation yesterday but had amb today
			row_today = result_today[j]
			x.append({"id": row_total[0], "total_dist": row_total[1], "total_dur": row_total[2], "total_amb": row_total[3], "room": row_total[4], "total_los": row_total[5], "pcu_los": row_total[6], "avg_amb": row_total[7], "today_dist": row_today[1], "today_dur": row_today[2], "today_amb": row_today[3], "yest_dist": 0, "yest_dur": 0, "yest_amb": 0})
			i = i + 1
			j = j + 1
		elif(k < len(result_yest) and id == result_yest[k][0]): 
			# when a patient didn't have ambulation today but had amb yesterday
			row_yest = result_yest[k]
			x.append({"id": row_total[0], "total_dist": row_total[1], "total_dur": row_total[2], "total_amb": row_total[3], "room": row_total[4], "total_los": row_total[5], "pcu_los": row_total[6], "avg_amb": row_total[7], "today_dist": 0, "today_dur": 0, "today_amb": 0, "yest_dist": row_yest[1], "yest_dur": row_yest[2], "yest_amb": row_yest[3]})
			i = i + 1
			k = k + 1
		else:
			# when a patient didn't have ambulation both today and yesterday
			x.append({"id": row_total[0], "total_dist": row_total[1], "total_dur": row_total[2], "total_amb": row_total[3], "room": row_total[4], "total_los": row_total[5], "pcu_loss": row_total[6], "avg_amb": row_total[7], "today_dist": 0, "today_dur": 0, "today_amb": 0, "yest_dist": 0, "yest_dur": 0, "yest_amb": 0})
			i = i + 1
	# sort the list by room number
	x = sorted(x, key = lambda i: i['room'])
	resp = jsonify(x)
	return resp




