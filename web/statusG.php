<?php
//https://www.dyclassroom.com/chartjs/chartjs-how-to-draw-bar-graph-using-data-from-mysql-table-and-php
//setting header to json
header('Content-Type: application/json');

//database
include 'credentials.php';

//query to get data from the table
$query = sprintf("SELECT sum(order_data.sheets) as sheets, deliver.name FROM `order_data` 
INNER JOIN deliver ON order_data.order_number=deliver.order_number 
WHERE  order_data.status = 'NotStarted' OR  order_data.status LIKE '%%Ticket%%' OR  order_data.status LIKE '%%P1%%'
GROUP BY deliver.name HAVING sum(order_data.sheets) > 0");

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
