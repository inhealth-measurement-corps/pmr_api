<?php
include 'connect.php';

$patient_room = $_POST["room"];
$date = $_POST["date"];
$table = 'live_details';

$sql = "SELECT patient_room as room, distance, duration, speed
FROM $table
WHERE start_datetime = 
(SELECT max(start_datetime) from $table 
where patient_room = '$patient_room')";

$result = $con->query($sql);
echo 'current'.'<br>';
if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
      echo $row["room"].'<>'.$row["distance"].'<>'.$row["duration"].'<>'.
            $row["speed"].'<br>';
  }
} else {
  echo '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
}
$con->close();
?>
