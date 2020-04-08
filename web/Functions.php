<?php
#Gets the Order Name, from the Order Number
function OrderName($Folders, $ONumber)
{
  foreach ($Folders as $i) {
    if (strstr($i, $ONumber)) {
      return $i;
    } else {
      return "Job Does not Exist, or is not Downloaded";
    }
  }
}
#Gets a list of all the Orders Downloaded
function JSONread($folder, $foldername)
{
  // load file
  $data = file_get_contents($folder . "/" . $foldername . "/" . $foldername . '.json');
  // decode json to associative array
  $json_arr = json_decode($data, true);
  //  var_dump($json_arr);
  echo  $json_arr["Ran"];
  //foreach ($json_arr as $key => $value) {
  //  echo  $json_arr[$key] . " : " .  $json_arr[$value] . "<br/>";
  //};
  return $json_arr;
}
function FolderList($folder)
{
  $Stripped_List = [];
  $fileList = glob($folder . "/*");  # Gathers all the Folders
  foreach ($fileList as $file) {
    array_push($Stripped_List, basename($file)); #Strips file path to base name.
  }
  return $Stripped_List; # Returns the Stripped List to Main Function
}
#Gets all the files from within the respective folder
function FilesList($folder, $OName)
{
  $Stripped_List = [];
  $fileList = glob($folder . "/" . $OName . "/*.pdf");  # Gathers all the Files
  foreach ($fileList as $file) {
    array_push($Stripped_List, basename($file)); #Strips file path to base name.
  }
  return $Stripped_List;  # Returns the Stripped List to Main Function
}
function File_Information($folder, $Folders, $OName, $Files)
{
  echo "<br> Order Name: " . $OName . "<br>";
  echo "<br>";
  $POS = 0;
  #Grabs the Page Counts for all the Files, and displays all the file names a well.
  foreach ($Files as $files) {
    $POS += 1;
    exec('/usr/bin/pdfinfo "' . $folder . "/" . $OName . "/" . $files . '" | awk \'/Pages/ {print $2}\'', $pages);
    echo  "File: " . $POS . " Page Count: <p style='color: #ff5252; display: inline'>" . $pages[$POS - 1] . "</p>: File Name: " . $files . "<br>";
  }
}
function CanRun($JobInfo)
{
  if ($JobInfo["Ran"] == "True")
    return false;
  if ($JobInfo["Collation"] == "UnCollated")
    return false;
  if ($JobInfo["Special Instructions"])
    return false;
  if ($JobInfo["Stapling"] == "Double Left - portrait")
    return false;
  if ($JobInfo["Front Cover"])
    return false;
  if ($JobInfo["Back Cover"])
    return false;
  return true;
}
