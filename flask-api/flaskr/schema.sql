DROP TABLE IF EXISTS live_details;
DROP TABLE IF EXISTS patient_info;

CREATE TABLE live_details (
    patient_ID INTEGER,
    ambulation INTEGER,
    amb_date DATE,
    time_of_day TIME,
    distance DECIMAL,
    duration DECIMAL,
    speed DECIMAL
);


CREATE TABLE patient_info (
   patient_ID INTEGER,
   room_number INTEGER,
   admission_date DATE,
   transfer_date DATE,
   discharge_date DATE,
   length_of_stay INTEGER
);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(500, 2, '2019-05-01', '12:38:00', 246.04, 254, 0.6591);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(500, 1, '2019-05-02', '11:46:00', 486.96, 292, 1.1367);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(500, 2, '2019-04-30', '11:52:00', 486.96, 517, 0.6421);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(500, 1, '2019-04-29', '15:17:00', 246.04, 212, 0.7895);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(124, 3, '2019-05-02', '14:38:00', 362.48, 154, 1.5978);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(124, 2, '2019-02-06', '15:18:00', 492.08, 362, 0.9243);

INSERT INTO live_details
(patient_ID, ambulation, amb_date, time_of_day, distance, duration, speed)
VALUES(124, 1, '2019-02-04', '15:20:00', 486.96, 536, 0.6191);

INSERT INTO patient_info
(patient_ID, room_number, admission_date, transfer_date, discharge_date, length_of_stay)
VALUES('500', 6, '2019-04-15', '2019-04-20', NULL, NULL);

INSERT INTO patient_info
(patient_ID, room_number, admission_date, transfer_date, discharge_date, length_of_stay)
VALUES('124', 18, '2019-01-22', '2019-02-01', NULL, 0);



