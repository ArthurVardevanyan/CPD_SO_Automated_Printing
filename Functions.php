<?php
function FolderList($folder){
      $Stripped_List = [];
      $fileList = glob($folder . "/*");  # Gathers all the Files
      foreach($fileList as $file){
           array_push($Stripped_List, basename($file));
         }
    return $Stripped_List; # Returns the Stripped List to Main Function

}
function OrderName($Folders, $ONumber){

  foreach ($Folders as $i)
  {
      if (strstr($i, $ONumber))
      {
          return $i;
        }
    }
}

function FilesList($folder, $OName)
{
  $Stripped_List = [];
    $fileList = glob($folder."/".$OName."/*.pdf");  # Gathers all the Files
    foreach($fileList as $file){
         array_push($Stripped_List, basename($file));
       }
    return $Stripped_List;  # Returns the Stripped List to Main Function
}



function File_Information($folder, $Folders,$OName,$Files){

          echo"<br> Order Name: ". $OName . "<br>";
          echo"<br>";
          $POS = 0;
          foreach($Files as $files){
            $POS += 1;
            exec('/usr/bin/pdfinfo "'.$folder."/".$OName."/".$files.'" | awk \'/Pages/ {print $2}\'', $pages);
            echo  "File: " . $POS . " Page Count: <p style='color: #ff5252; display: inline'>" . $pages[$POS-1]. "</p>: File Name: " . $files ."<br>";


}

}











?>
