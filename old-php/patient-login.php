<?php
    $host = 'localhost';
    $server_username = 'jessie';
    $server_password = 'rJvMXazyFrZCw7O4'; 
    $db = 'mmambulation';
    $table = 'patient_info';

    $con = mysqli_connect($host, $server_username, $server_password, $db) 
            or die ('Unable to connect');

    if (mysqli_connect_error($con)) {
        echo "Failed to connect to MySQL: " . mysqli_connect_error();
    }

    $patient_username = $_POST['username'];
    $patient_password = $_POST['password'];
    $server_password = "";

    unset($result_array);
    $sql = "SELECT password FROM $table 
        WHERE username = '$patient_username'";
    
    $result = $con->query($sql);
    $valid = false;

    if ($result->num_rows > 0) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            $server_password = $row["password"];
        }
    } 

    if ($server_password == $patient_password) {
        $valid = true;
    }

    // If the user can log in to the server, get other information as well
    if ($valid) {
        $result->valid = true;
        $sql = "SELECT patient_ID FROM $table 
            WHERE username = '$patient_username'";
        $result = $con->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $result_array ->id = $row["patient_ID"];
            }
        } else {
            // Should never get here since name is NON-NULL
            $result_array ->id = "None";
        }

        $sql = "SELECT room_number FROM $table 
            WHERE username = '$patient_username'";
        $result = $con->query($sql);
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) { 
                $result_array ->room = $row["room_number"];
            }
        } else {
            // Should never get here since name is NON-NULL
            $result_array ->room = "None";
        }
    } else {
        $result->valid = false;
    }
    $json = json_encode($result_array);
    echo $json;
    $con->close();
?>