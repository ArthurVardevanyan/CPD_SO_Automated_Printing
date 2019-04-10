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
<h2>School Order Printer Rev APRIL FOOLS</h2>
<form action='index.php' method='post'>
  <h3>File Info</h3>
  <input type="Number" name="OrderNumber" min="0" required>Order Number<br>
  <input type='submit' name='FI' value='File Info'>
  <input type='submit' name='FIO' value='File Info /w open files'><br><br><br>
</form>
<form action='index.php' method='post'>
  <h3>File Operation</h3>
  <input type="Number" name="OrderNumber" min="0" required>Order Number<br>
  <input type='hidden' value='0' name='Collation'>
  <input type="radio" name="Collation" value="0" id="Collated" checked><label for="Collated">Collated</label>
  <input type="radio" name="Collation" value="1" id="UnCollated"><label for="UnCollated">UnCollated (No SlipSheets)</label><br>
  <input type='hidden' value='0' name='Speed'>
  <input type="radio" name="Speed" value="1" id="High Speed" checked><label for="High Speed">High Speed</label>
  <input type="radio" name="Speed" value="2" id="High Resolution"><label for="High Resolution">High Resolution</label><br>
  <input type='hidden' value='0' name='Duplex'>
  <input type="checkbox" name="Duplex" value="1" id="DuplexL" class="DuplexL" onclick="if(this.checked) {document.getElementById('DuplexS').checked=false;}" ><label for="DuplexL">DuplexL</label>
  <input type="checkbox" name="Duplex" value="2" id="DuplexS" class="DuplexS" onclick="if(this.checked) {document.getElementById('DuplexL').checked=false;}"><label for="DuplexS">DuplexS</label><br>
  <input type='hidden' value='0' name='Staple'>
  <input type="checkbox" name="Staple" value="1" id="SingleStaple" clas="SingleStaple" onclick="if(this.checked) {document.getElementById('DualStaple').checked=false;}"><label for="SingleStaple">Staple</label>
  <input type="checkbox" name="Staple" value="2" id="DualStaple" class="DualStaple" onclick="if(this.checked) {document.getElementById('SingleStaple').checked=false;}"><label for="DualStaple">Dual Staple</label><br>
  <input type='hidden' value='0' name='Punch'>
  <input type="checkbox" name="Punch" value="1" id="Punch"><label for="Punch">Punch</label><br>
  <input type='hidden' value='0' name='OffSet'>
  <input type="checkbox" name="OffSet" value="1" id="OffSet" checked><label for="OffSet">OffSet</label><br>
  <input type="Number" name="TC"  min="0" required>Total Copies <br>
  <input type="Number" name="SETS" value="1" min="0" required>Sets <br>
  <input type="Number" name="CP" min="0" max="999" required>Copies Per Set<br>

        <input type='submit' name='RUN' value='RUN'><br>
    </form><br><br><br>
    <?php
    include 'Functions.php';
    $folder = "School Orders";

if (isset($_POST['FI'])) #When just the INFO button is prssed, it gets the file info.
          {
            $ONumber = $_POST['OrderNumber'];
            $Folders =  FolderList($folder);
            $OName =  OrderName($Folders, $ONumber);
            $Files = FilesList($folder, $OName);
            File_Information($folder, $Folders,$OName,$Files);
          }
if (isset($_POST['FIO'])) #Same as Info Button, but opens all the files.
          {
            $ONumber = $_POST['OrderNumber'];
            $Folders =  FolderList($folder);
            $OName =  OrderName($Folders, $ONumber);
            $Files = FilesList($folder, $OName);
            File_Information($folder, $Folders,$OName,$Files);
            foreach( $Files as $files){
                    echo '<script type="text/javascript">',
            'openNewBackgroundTab("'.$folder."/".$OName."/".$files.'");',
            '</script>';
          }
          }


if (isset($_POST['RUN']))#This setups up the linux cups command with the correct paramters to send to the printer.
      {

        #Command List
        $ONumber = $_POST['OrderNumber'];
        $Collate = ["-o Collate=True","-o Collate=False"];
        $speed = ["", "-o XROutputMode=HighSpeed", "-o XROutputMode=HighResolution"];
        $sides = ["", "-o sides=two-sided-long-edge","-o sides=two-sided-short-edge"];
        $staple = ["", "-o XRStapleOption=SinglePortrait", "-o XRStapleOption=DualPortrait"];
        $punch = ["", "-o XRPunchOption=3Punch"];
        $OffSet = ["-o XRRequestOffset=None", ""];
        $QTYA = [];
        $TotalQTY = $_POST['TC'];
        $SETS= (int)$_POST['SETS'];
        $QTY= (int)$_POST['CP'];
        $Duplex = $_POST['Duplex'];
        $HP = $_POST['Punch'];
        $S = $_POST['Staple'];

        echo "Duplex        : " . $_POST['Duplex'] . "<br>";
        echo "Hole Punch    : " . $_POST['Punch']  . "<br>";
        echo "Stapling      : " . $_POST['Staple']  . "<br>";
        echo "Total Copies  : " . $TotalQTY  . "<br>";
        echo "Number of Sets: " .  $SETS.  "<br>";
        echo "Copie(s) Per Set: " . $QTY . "<br>";

        $Folders =  FolderList($folder);
        $OName =  OrderName($Folders, $ONumber);
        $Files = FilesList($folder, $OName);
        File_Information($folder, $Folders,$OName,$Files);

        #Some math to determine how many times to send the job and at what quantities.
          if($TotalQTY == $QTY*$SETS){
              for($x = 0; $x <  $SETS ; $x++)
              {
              array_push($QTYA, $QTY);
            }
          }
          else
          {
              array_push($QTYA, $QTY);
              for ($x = 0; $x < ($SETS-1); $x++){
                  if($TotalQTY-$QTY > 0){
                      $TotalQTY = $TotalQTY-$QTY;
                      array_push($QTYA, $TotalQTY);
                    }
                  else{
                    array_push($QTYA, $TotalQTY);

                    }
            }
          }
          #Display & Sends the commands to the printer
            for($x = 0; $x < $SETS ; $x++){
              foreach( $Files as $files){
                echo "<br>";
                echo "lpr -#" . (string)$QTYA[$x] . " " . $staple[$S] . " " . $punch[$HP] . "  " . $sides[$Duplex] . "  " . '"' .$folder."/".$OName."/".$files.'"';
              }
              }

                for($x = 0; $x < $SETS ; $x++){
                  foreach( $Files as $files){
                $output = "lpr -#" . (string)$QTYA[$x] . " " . $staple[$S] . " " . $punch[$HP] . "  " . $sides[$Duplex] . "  " . '"' .$folder."/".$OName."/".$files.'" > /dev/null 2>&1 &';
                exec($output);

            }
            }
      }
?>
      </body>
      </html>
