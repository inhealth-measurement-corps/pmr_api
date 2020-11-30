<?php
include 'connect.php';

$room_number = $_POST["room_number"];
$date = $_POST["date"];
$table = 'live_details';
$info_table = 'patient_info';
$patient_id = array();

$sql = "SELECT patient_ID FROM $info_table
where room_number = $room_number";
$result = $con->query($sql);
$index = 0;
if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
      $patient_id[$index] = $row['patient_ID'];
      $index = $index + 1;
  }
}

$active_patient = 113;

$sql = "SELECT time_of_day, distance, speed FROM $table 
WHERE patient_ID = '$active_patient' and date = $date";

// No need to convert this speed because it is in mph already
$result = $con->query($sql);
echo "today".'<br>';
if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
      echo $row["time"].'<>'.$row["distance"].'<>'.$row["speed"].'<br>';
  }
} else {
  echo '0'.'<>'.'0'.'<>'.'0'.'<br>';
}
$con->close();
?>
