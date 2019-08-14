<?php
session_start(); #Prevents Reset of Login State
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>CPD SO Printing</title>
  <link rel='icon' href='images/favicon.ico' type='image/x-icon'/ >
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<link rel="stylesheet" type="text/css" href="/main.css">
<script src="js.js"></script>

<script>
if ( window.history.replaceState ) {  //Makes Redirects After Html Forms not leave data in url.
    window.history.replaceState( null, null, window.location.href );
}
</script></head>
<h2>School Order Printer Rev 20190814</h2>
<form action='index.php' method='post'>
  <h3>File Info</h3>
  <input type="Number" name="OrderNumber" min="0" required>Order Number<br>
  <input type='submit' name='FI' value='File Info'>
  <input type='submit' name='FIO' value='File Info /w open files'><br><br><br>
</form>


    <br><br><br>
    <?php
include 'Functions.php';
$folder = "School_Orders";

if (isset($_POST['FI'])) #When just the INFO button is prssed, it gets the file info.
{
    $ONumber = $_POST['OrderNumber'];
    $Folders = FolderList($folder);
    $OName = OrderName($Folders, $ONumber);
    $Files = FilesList($folder, $OName);
    File_Information($folder, $Folders, $OName, $Files);
    $JobData = JSONread($folder, $OName);
}
if (isset($_POST['FIO'])) #Same as Info Button, but opens all the files.
{
    $ONumber = $_POST['OrderNumber'];
    $Folders = FolderList($folder);
    $OName = OrderName($Folders, $ONumber);
    $Files = FilesList($folder, $OName);
    File_Information($folder, $Folders, $OName, $Files);
    foreach ($Files as $files) {
        echo '<script type="text/javascript">',
        'openNewBackgroundTab("' . $folder . "/" . $OName . "/" . $files . '");',
            '</script>';
    }
}
$Folders = FolderList($folder);

foreach( $Folders as $Folder)
  echo $Folder . " <br>";
?>
      </body>
      </html>
