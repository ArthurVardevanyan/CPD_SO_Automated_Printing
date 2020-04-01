<?php
//https://www.dyclassroom.com/chartjs/chartjs-how-to-draw-bar-graph-using-data-from-mysql-table-and-php
//setting header to json
header('Content-Type: application/json');
//database
include 'credentials.php';
//query to get data from the table
$query = sprintf("SELECT `email_id`, `order_number`, `status`, `order_subject` FROM `order_data` ORDER BY `order_number` ");
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
