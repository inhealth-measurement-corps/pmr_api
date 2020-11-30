<?php
include 'connect.php';
$today = $_POST['today'];

// $today = '2018-07-18';

$date = date_create($today);
// subtract one day from today
$date->sub(new DateInterval('P1D'));
$yest_start = $date->format('Y-m-d');
$table = 'details';

$yest_end = $yest_start.' 23:59:59';

// Be able to grab all and today info
$sql = "SELECT TOTAL.id AS id, TOTAL.room AS room, TOTAL.distance AS total_distance, TOTAL.duration AS total_duration, TOTAL.ambulation AS total_ambulation, TOTAL.los AS total_los, 
TODAY.today_distance AS today_distance, TODAY.today_duration AS today_duration,
TODAY.today_ambulation AS today_ambulation, 
YEST.yest_distance AS yest_distance, YEST.yest_duration AS yest_duration,
YEST.yest_ambulation AS yest_ambulation
FROM
(SELECT patient_number AS id , patient_room AS room, sum(distance) 
AS distance, sum(duration) AS duration, count(total_ambulation) AS ambulation,
datediff(max(date_update_time), min(start_datetime)) AS los
FROM $table 
GROUP BY patient_room) AS TOTAL
LEFT JOIN
(SELECT patient_room AS room, sum(distance) AS today_distance, 
sum(duration) AS today_duration, max(daily_ambulation) AS today_ambulation
FROM $table 
WHERE start_datetime >= '$today' 
GROUP BY patient_room) AS TODAY
ON TOTAL.room = TODAY.room
LEFT JOIN
(SELECT patient_room AS room, sum(distance) AS yest_distance, 
sum(duration) AS yest_duration, max(daily_ambulation) AS yest_ambulation
FROM $table WHERE start_datetime BETWEEN '$yest_start' AND '$yest_end' 
GROUP BY patient_room) AS YEST
ON TOTAL.room = YEST.room";


$result = $con->query($sql);


$table = array();


if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
    $table[] = $row;
  }
} 

$index = 0;
$myArr = array();
while($index < count($table)) {
$patient = $table[$index];
unset($patient_info);
$patient_info ->id = $patient["id"];
$patient_info ->room = $patient["room"];

if(is_null($patient["total_distance"])) {
  $patient_info ->total_dist = "0";
} else {
$patient_info ->total_dist = $patient["total_distance"];
}
if(is_null($patient["total_duration"])) {
  $patient_info ->total_dur = "0";
} else {
$patient_info ->total_dur = $patient["total_duration"];
}
if(is_null($patient["total_ambulation"])) {
  $patient_info ->total_amb = "0";
} else {
$patient_info ->total_amb = $patient["total_ambulation"];
}
if(is_null($patient["total_los"])) {
  $patient_info ->total_los = "0";
} else {
$patient_info ->total_los = $patient["total_los"];
}

if(is_null($patient["today_distance"])) {
  $patient_info ->today_dist = "0";
} else {
$patient_info ->today_dist = $patient["today_distance"];
}
if(is_null($patient["today_duration"])) {
  $patient_info ->today_dur = "0";
} else {
$patient_info ->today_dur = $patient["today_duration"];
}
if(is_null($patient["today_ambulation"])) {
  $patient_info ->today_amb = "0";
} else {
$patient_info ->today_amb = $patient["today_ambulation"];
}
if(is_null($patient["yest_distance"])) {
  $patient_info ->yest_dist = "0";
} else {
$patient_info ->yest_dist = $patient["yest_distance"];
}
if(is_null($patient["yest_duration"])) {
  $patient_info ->yest_dur = "0";
} else {
$patient_info ->yest_dur = $patient["yest_duration"];
}
if(is_null($patient["yest_ambulation"])) {
  $patient_info ->yest_amb = "0";
} else {
$patient_info ->yest_amb = $patient["yest_ambulation"];
}

$myArr[$index] = $patient_info;
$index++;
}
$myJSON = json_encode($myArr);

echo $myJSON;

$con->close();
?>