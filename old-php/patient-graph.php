<?php
    $host = 'localhost';
    $server_username = 'jessie';
    $server_password = 'rJvMXazyFrZCw7O4'; 
    $db = 'mmambulation';
    $table = 'live_details';

    $con = mysqli_connect($host, $server_username, $server_password, $db) 
            or die ('Unable to connect');

    if (mysqli_connect_error($con)) {
        echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }

    $patient_id = $_POST['patient_id'];
    $type = $_POST['type'];
    
    // Find the start date first to make sure it's the correct patient
    $sql = "SELECT transfer_date as start_datetime 
        FROM patient_info
        WHERE patient_ID = $patient_id";

    $start = "";
    $result = $con->query($sql);
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $start = $row["start_datetime"];
        }
    }
    $result_array = array();
    $sql = "";
    
    if ($type == 'ambulation') {
        $sql = "SELECT date, count(ambulation) as result
        FROM $table 
        WHERE (patient_id = '$patient_id' and 
        date >= '$start')
        GROUP BY date";
    } else if ($type == 'distance') {
        $sql = "SELECT date, sum(distance) as result
        FROM $table
        WHERE (patient_id = $patient_id and 
        date >= '$start')
        GROUP BY date";
    } else {
        // $type == 'speed'
        $sql = "SELECT date, sum(distance)/sum(duration) as result
        FROM $table 
        WHERE (patient_id = '$patient_id' and 
        date >= '$start')
        GROUP BY date";
    }
    
    $index = 0;
    $result = $con->query($sql);
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            unset($result_value);
            
            $result_value->date = $row["date"];
            $result_value->result = $row["result"];
            $result_array[$index] = $result_value;
            $index++;
        }
    }

    $json = json_encode($result_array);
    echo $json;
    $con->close();
?>
