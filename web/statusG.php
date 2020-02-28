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
$query = sprintf("SELECT sum(order_data.sheets) as sheets, deliver.name FROM `order_data` INNER JOIN deliver ON order_data.order_number=deliver.order_number GROUP BY deliver.name");

//execute query
$result = $mysqli->query($query);

//loop through the returned data
$data = array();
foreach ($result as $row) {
  $data[] = $row;
}

//free memory associated with result
$result->close();

//close connection
$mysqli->close();

//now print the data

print json_encode($data);
