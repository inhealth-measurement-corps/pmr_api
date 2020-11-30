<?php
include 'connect.php';

$patient_room = $_POST["patient_room"];
$date = $_POST["date"];
$table = 'live_details';

$sql = "SELECT dayofmonth(start_datetime) as dayofmonth,
sum(distance) as distance, sum(distance)/sum(duration) as speed
FROM $table 
WHERE patient_room = '$patient_room'
and start_datetime between DATE_FORMAT('$date' ,'%Y-%m-01') AND '$date'
GROUP BY CAST(start_datetime as DATE) ";

$result = $con->query($sql);
echo "month".'<br>';
if ($result->num_rows > 0) {
  while ($row = $result->fetch_assoc()) {
      echo $row["dayofmonth"].'<>'.$row["distance"].'<>'.$row["speed"].'<br>';
  }
} else {
  echo "0".'<>'.'0'.'<>'.'0'.'<br>';
}
$con->close();
?>
