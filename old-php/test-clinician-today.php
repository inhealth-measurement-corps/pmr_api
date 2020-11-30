<?php
include 'connect.php';

$patient_room = $_POST["patient_room"];
$start_time = $_POST["date"];
$end_time = $start_time.' 23:59:59';
$table = 'details';


$sql = "SELECT time_to_sec(CAST(start_datetime as TIME))/(60*60) as time, 
distance, speed
FROM $table 
WHERE patient_room = '$patient_room' and 
start_datetime between '$start_time' and '$end_time'
GROUP BY CAST(start_datetime as TIME)";

// No need to convert this speed because it is in mph already
$result = $con->query($sql);

$index = 0;
$day_array = array();

if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		
		unset($day_data);
		
        if(is_null($row["time"])) {
			$day_data ->date="0";
		} else {
		$day_data ->date=$row["time"];
	}
	    if(is_null($row["distance"])) {
	    	$day_data ->distance="0";
	    } else {
		$day_data ->distance=$row["distance"];
	}
	    if(is_null($row["speed"])) {
		 $day_data ->speed="0.0";
	}  else {
       $day_data ->speed=$row["speed"];
	}

		$day_array[$index] = $day_data;

		$index++;
	}
}

$myJSON = json_encode($day_array);
echo $myJSON;

$con->close();
?>