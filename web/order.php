<?php

function curPageURL()
{
  //https://stackoverflow.com/questions/5598480/php-parse-current-url
  $pageURL = 'http';
  if ($_SERVER["HTTPS"] == "on") {
    $pageURL .= "s";
  }
  $pageURL .= "://";
  if ($_SERVER["SERVER_PORT"] != "80") {
    $pageURL .= $_SERVER["SERVER_NAME"] . ":" . $_SERVER["SERVER_PORT"] . $_SERVER["REQUEST_URI"];
  } else {
    $pageURL .= $_SERVER["SERVER_NAME"] . $_SERVER["REQUEST_URI"];
  }
  return $pageURL;
}

$url_components = parse_url(curPageURL());
parse_str($url_components['query'], $params);

//https://www.dyclassroom.com/chartjs/chartjs-how-to-draw-bar-graph-using-data-from-mysql-table-and-php
//setting header to json

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
$query = sprintf('SELECT * FROM `order_data` where `email_id` = "' . $params['id'] . '"');

//execute query
$result = $mysqli->query($query);

$data = array();

foreach ($result as $row) {
  $data[] = $row;
}

$result->close();

$queryF = sprintf('SELECT file_number, name, pages FROM files WHERE order_number = "' . $params['on'] . '"');

//execute query
$resultF = $mysqli->query($queryF);

$dataF = array();

foreach ($resultF as $row) {
  $dataF[] = $row;
}

$resultF->close();


$queryD = sprintf('SELECT name, address FROM `deliver` WHERE `order_number` = "' . $params['on'] . '"');

//execute query
$resultD = $mysqli->query($queryD);

$dataD = array();

foreach ($resultD as $row) {
  $dataD[] = $row;
}

$resultD->close();
$mysqli->close();



$columns = array();
//https://stackoverflow.com/questions/4353505/php-create-dynamic-html-table
echo ' <div style="width: 100%; text-align: left; float: center;">
<link rel="stylesheet" type="text/css" href="main.css"><table  id="t01">';
foreach ($data as $name => $values) {

  foreach ($values as $k => $v) {
    $columns[$k] = $k;
    echo "<tr>";
    echo "<th>$k</th>";
    echo "<td>$v</td>";
    echo "</tr>";
  }
}
echo "</tbody></table></div><br>";



$columns = array();
//https://stackoverflow.com/questions/4353505/php-create-dynamic-html-table
echo ' <div style="width: 100%; text-align: left; float: center;">
<link rel="stylesheet" type="text/css" href="main.css"><table  id="t01"><tbody>';
foreach ($dataD as $name => $values) {

  foreach ($values as $k => $v) {
    echo "<td>$v</td>";
    $columns[$k] = $k;
  }
  echo "</tr>";
}
echo "</tbody><thead><tr>";
foreach ($columns as $column) {
  echo "<th>$column</th>";
}
echo "</thead></table></div><br>";


$columns = array();
//https://stackoverflow.com/questions/4353505/php-create-dynamic-html-table
echo ' <div style="width: 100%; text-align: left; float: center;">
<link rel="stylesheet" type="text/css" href="main.css"><table  id="t01"><tbody>';
foreach ($dataF as $name => $values) {

  foreach ($values as $k => $v) {
    echo "<td>$v</td>";
    $columns[$k] = $k;
  }
  echo "</tr>";
}
echo "</tbody><thead><tr>";
foreach ($columns as $column) {
  echo "<th>$column</th>";
}
echo "</thead></table></div><br>";
