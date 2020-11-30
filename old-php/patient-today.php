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
    $date = $_POST['date'];
    unset($result_array);
    $result_array->type = "today";

    $sql = "SELECT sum(distance) as distance, sum(duration) as duration, 
        count(ambulation) as ambulation 
        FROM $table WHERE (patient_ID = '$patient_id' and 
        date = '$date' )";
    $result = $con->query($sql);
    if ($result->num_rows > 0) {
        $result_array->result = "valid";
        while ($row = $result->fetch_assoc()) {
            $result_array->distance = $row["distance"];
            $result_array->duration = $row["duration"];
            $result_array->ambulation = $row["ambulation"];
        }
    } else {
        $result_array->result = "None";
    }

    $json = json_encode($result_array);
    echo $json;
    $con->close();
?>
