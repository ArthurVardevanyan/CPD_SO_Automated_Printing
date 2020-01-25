<?php
session_start(); #Prevents Reset of Login State
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <title>CPD SO Printing</title>
  <link rel='icon' href='images/favicon.ico' type='image/x-icon'/ >
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script src="https://cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css">
<!--<link rel="stylesheet" type="text/css" href="main.css">-->

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
$folder = "SO";

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

$json = " ";

foreach( $Folders as $foldername){
#  echo $foldername . " <br>";
 if (file_exists ( $folder . "/" . $foldername ."/" . $foldername . '.json' )){

  $data = file_get_contents($folder . "/" . $foldername ."/" . $foldername . '.json');
  $json = $json . $data . ",\n";
};
}
$folder = $folder . "/Archive";
$Folders = FolderList($folder);


foreach( $Folders as $foldername){
#  echo $foldername . " <br>";
 if (file_exists ( $folder . "/" . $foldername ."/" . $foldername . '.json' )){

  $data = file_get_contents($folder . "/" . $foldername ."/" . $foldername . '.json');
  $json = $json . $data . ",\n";

  };

}
$jt = "[" . substr($json, 0, -2) . "]";

$json_a = json_decode($jt, true);

$a=array();

foreach ($json_a as $person_name => $person_a) {
    #echo $person_a['Date Ordered'] . "<br>";
    array_push($a,$person_a['Date Ordered']);
}
print_r(array_count_values($a));





?>
<script type="text/javascript">


$(document).ready(function() {

  var aDemoItems =  [<?php echo $json; ?> ];
//    var aDemoItems  = oResults.lDemographicItems; //
    var jsonString = JSON.stringify(aDemoItems  ) //for testing

   //Load  datatable
    var oTblReport = $("#tblReportResultsDemographics")

    oTblReport.DataTable ({
        data: aDemoItems,
        "columns" : [
            { "data" : "Order Number", "title" : "Order Number"},
            { "data" : "Order Subject", "title" : "Order Subject"},
            { "data" : "Date Ordered",  "title" : "Date Ordered"},
            { "data" : "First Name",  "title" : "First Name"},
            { "data" : "Last Name",  "title" : "Last Name"}



        ]
    });
});
</script>
<table id="tblReportResultsDemographics" class="display" width="100%"></table>

      </body>
      </html>
