<?php
include 'connect.php';

$patient_room = $_POST["patient_room"];
$date = $_POST["date"];
$table = 'details';

$sql = "SELECT dayofmonth(start_datetime) as dayofmonth,
sum(distance) as distance, sum(distance)/sum(duration) as speed
FROM $table 
WHERE patient_room = '$patient_room'
and start_datetime between DATE_FORMAT('$date' ,'%Y-%m-01') AND '$date'
GROUP BY CAST(start_datetime as DATE) ";

$result = $con->query($sql);

$index = 0;
if($result->num_rows > 0) {
	while($row = $result->fetch_assoc()) {
		unset($day_data);
		if(is_null($row["dayofmonth"])) {
			$day_data ->date="0";
		} else {
		$day_data ->date=$row["dayofmonth"];
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