<?php
//https://www.dyclassroom.com/chartjs/chartjs-how-to-draw-bar-graph-using-data-from-mysql-table-and-php
//setting header to json
header('Content-Type: application/json');

//database
define('DB_HOST', '127.0.0.1');
define('DB_USERNAME', 'CPD');
define('DB_PASSWORD', 'CPD');
define('DB_NAME', 'school_orders');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);

if (!$mysqli) {
  die("Connection failed: " . $mysqli->error);
}

//query to get data from the table
$query = sprintf("SELECT * FROM `order_data` WHERE `status` = 'NotStarted' OR `status` LIKE '%%Ticket%%' HAVING `sheets` > 0  ORDER BY `order_number`");
//execute query
$result = $mysqli->query($query);

//loop through the returned data
foreach ($result as $row) {
  $data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

//now print the data

print json_encode($data);
