<!doctype html>
<html>

<head>
    <title>CPD SO Printing</title>

</head>

<body>


    <h2>School Order Printer Rev 20200131</h2>
    <form action='webPrint.php' method='post'>
        <h3>File Info</h3>
        <input type="Number" name="OrderNumber" min="0" required>Order Number<br>
        <input type='submit' name='FI' value='Print /w Email in Basic AutoRun Mode'>
    </form>
    <?php

    if (isset($_POST['FI'])) {
        $ONumber = $_POST['OrderNumber'];
        $cmd = 'webPrint.exe ' . $ONumber . " SO/ 1 False True False False False False";
        $command = escapeshellcmd($cmd);
        $output = shell_exec($command);
        echo $output;
    }
    ?>
</body>

</html>