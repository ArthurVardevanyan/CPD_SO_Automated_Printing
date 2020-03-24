<?php
define('DB_HOST', '127.0.0.1');
define('DB_USERNAME', 'CPD');
define('DB_PASSWORD', 'CPD');
define('DB_NAME', 'school_orders');
//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);
if (!$mysqli) {
    die("Connection failed: " . $mysqli->error);
}
