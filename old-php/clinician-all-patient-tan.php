<?php
include 'connect.php';
$today = $_POST['today'];

$date = date_create($today);
$date->sub(new DateInterval('P1D'));
$yest_start = $date->format('Y-m-d');
$table = 'live_details';

$yest_end = $yest_start.' 23:59:59';
// Be able to grab all and today info

echo "all<br>";

$sql_total = "SELECT patient_number as id , patient_room as room, sum(distance) 
as distance, sum(duration) as duration, count(total_ambulation) as ambulation,
datediff(max(date_update_time), min(start_datetime)) as los
FROM $table group by patient_room";

$sql_today = "SELECT patient_room as room, sum(distance) as today_distance, 
sum(duration) as today_duration, max(daily_ambulation) as daily_ambulation
from $table where start_datetime >= '$today' group by patient_room";

$sql_yesterday = "SELECT patient_room as room, sum(distance) as yest_distance, 
sum(duration) as yest_duration
from $table where start_datetime between'$yest_start' and '$yest_end' 
group by patient_room";

$result_total = $con->query($sql_total);
$result_today = $con->query($sql_today);
$result_yest = $con->query($sql_yesterday);

$table_total = array();
$table_today = array();
$table_yest = array();

if ($result_total->num_rows > 0) {
  while ($row = $result_total->fetch_assoc()) {
    $table_total[] = $row;
  }
} 

if ($result_today->num_rows > 0) {
  while($row = $result_today->fetch_assoc()) {
    $table_today[] = $row;
  }
}

if ($result_yest->num_rows > 0) {
  while($row = $result_yest->fetch_assoc()) {
    $table_yest[] = $row;
  }
}

$today_index = 0;
$total_index = 0;
$yest_index = 0;

// If the index is in total, it has to be in today and yesterday.
// All of the room is sorted so should be good
if (count($table_total) != 0){
  while ($total_index < count($table_total)) {
    $total_room = $table_total[$total_index]["room"];
    $today_room = $table_today[$today_index]["room"];
    $yest_room = $table_yest[$yest_index]["room"];
    // echo "Today".$today_room.'<br>';
    // echo "yesterday".$yest_room.'<br>';
    // echo "Total".$total_room.'<br>';
    // No value for today and yesterday
    if ($today_index >= count($table_today) && $yest_index >= count($table_yest)) {
      echo $table_total[$total_index]["id"].'<>'.
          $table_total[$total_index]["room"].'<>'.
          $table_total[$total_index]["distance"].'<>'.
          $table_total[$total_index]["duration"].'<>'.
          $table_total[$total_index]["ambulation"].'<>'.
          $table_total[$total_index]["los"].'<>'.
          '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
    } else if ($today_index >= count($table_today)) { 
      if ($total_room == $yest_room) {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        '0'.'<>'.'0'.'<>'.'0'.'<>'.$table_yest[$yest_index]["yest_distance"].'<>'.
        $table_yest[$yest_index]["yest_duration"].'<br>';
        $yest_index++;
      } else {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
      }
    } else if ($yest_index >= count($table_yest)) {

      if ($total_room == $today_room) {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        $table_today[$today_index]["today_distance"].'<>'.
        $table_today[$today_index]["today_duration"].'<>'.
        $table_today[$today_index]["daily_ambulation"].'<>'.
        '0'.'<>'.'0'.'<br>';
        $today_index++;
      } else {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
      }
    } else {
      if (($today_room == $total_room)) {
        if ($yest_room == $total_room) {
          echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        $table_today[$today_index]["today_distance"].'<>'.
        $table_today[$today_index]["today_duration"].'<>'.
        $table_today[$today_index]["daily_ambulation"].'<>'.
        $table_yest[$yest_index]["yest_distance"].'<>'.
        $table_yest[$yest_index]["yest_duration"].'<br>';
        $today_index++;
        $yest_index++;
        } else {
          echo $table_total[$total_index]["id"].'<>'.
          $table_total[$total_index]["room"].'<>'.
          $table_total[$total_index]["distance"].'<>'.
          $table_total[$total_index]["duration"].'<>'.
          $table_total[$total_index]["ambulation"].'<>'.
          $table_total[$total_index]["los"].'<>'.
          $table_today[$today_index]["today_distance"].'<>'.
          $table_today[$today_index]["today_duration"].'<>'.
          $table_today[$today_index]["daily_ambulation"].'<>'.
          '0'.'<>'.'0'.'<br>';
          $today_index++;
        }
      } else if ($total_room == $yest_room) {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        '0'.'<>'.'0'.'<>'.'0'.'<>'.$table_yest[$yest_index]["yest_distance"].
        '<>'.$table_yest[$yest_index]["yest_duration"].'<br>';
        $yest_index++;
      } else {
        echo $table_total[$total_index]["id"].'<>'.
        $table_total[$total_index]["room"].'<>'.
        $table_total[$total_index]["distance"].'<>'.
        $table_total[$total_index]["duration"].'<>'.
        $table_total[$total_index]["ambulation"].'<>'.
        $table_total[$total_index]["los"].'<>'.
        '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
      }
    }
    $total_index += 1;
  }
} else {
  echo '0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.'<>'.'0'.
      '<>'.'0'.'<>'.'0'.'<>'.'0'.'<br>';
}
$con->close();
?>
