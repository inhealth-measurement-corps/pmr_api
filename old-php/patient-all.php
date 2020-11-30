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
    $start_date = "";

    $sql = "SELECT transfer_date as start_datetime
    FROM patient_info
    WHERE (patient_ID = '$patient_id')";

    $result = $con->query($sql);
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $start_date = $row["start_datetime"];
        }
    }
    unset($result_array);
    $result_array->start = $start_date;
    $result_array->type = "all";

    $sql = "SELECT sum(distance) as distance, sum(duration) as duration, 
    count(ambulation) as ambulation, max(date) as end_datetime
    FROM $table
    WHERE (patient_ID = '$patient_id')";

    $result = $con->query($sql);
    if ($result->num_rows > 0) {
        $result_array->result = "valid";
        while ($row = $result->fetch_assoc()) {
            $result_array->distance = $row["distance"];
            $result_array->duration = $row["duration"];
            $result_array->ambulation = $row["ambulation"];
            $result_array->end = $row["end_datetime"];
        }
    } else {
        $result_array->result = "None";
    }

    $json = json_encode($result_array);
    echo $json;
    $con->close();
?>
