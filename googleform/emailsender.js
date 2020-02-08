function EmailSender(e) {
    var myEmail = "";
    var myOtherEmail = "";

    var subject = e.values[3] + " " + e.values[2] + " - NAME - " + e.values[5];
    var thierEmail = e.values[1]
    var htmlBody = "";
    var textBody = "";

    var values = e.values;
    var ss = SpreadsheetApp.getActive();
    var sheet = ss.getSheetByName('Form Responses 1');

    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues();
    var currentrow = sheet.getLastRow();
    var htmlBody = "<p>Your copy job has been submitted as shown below:</p><br><b>Order Number: " + ("00000" + currentrow).slice(-5) + "</b><br>";
    var textBody = "\n\n\nYour copy job has been submitted as shown below:\n\nOrder Number: " + ("00000" + currentrow).slice(-5) + "\n"

    htmlBody += '<head><style>tr:nth-child(even) {background-color: #f2f2f2;} </style> </head> <table style="border-radius:2px;margin:20px 0 25px;min-width:400px;border:1px solid #eee" cellspacing="0" cellpadding="10" border="0">';
    var rowCount = 0

    for (var i = 0; i < values.length; i++) {
        var label = headers[0][i];
        var data = values[i];
        if (rowCount % 2 == 0)
            var tr = '<tr style="background:#f9f9f9">';
        else
            var tr = '<tr>';
        if (data != "") {
            if (label.indexOf('Attach your file(s) in PDF format.') == -1) {

                htmlBody += tr + '<td style="font-weight:bold;border-bottom:1px solid #eee;width:180px"><b>' + label + '</b></td><td style="border-bottom:1px solid #eee">' + data + '</td></tr>';
                textBody += label + " " + data + "\n";
                rowCount += 1;
            }
            else {
                var filedata = "";
                var textFileData = "";
                var array = data.split(',');
                for (var j = 0; j < array.length; j++) {
                    filedata += '<a href="' + array[j] + '">File ' + (j + 1) + '</a><br>';
                    textFileData += "File " + (j + 1) + " " + array[j] + "\n"
                }
                htmlBody += tr + '<td style="font-weight:bold;border-bottom:1px solid #eee;width:180px"><b>' + label + '</b></td><td style="border-bottom:1px solid #eee">' + filedata + '</td></tr>';
                textBody += label + " " + textFileData;
                rowCount += 1;
            }
        }

    };
    htmlBody += '</table>                                                                                                                                                                                                                                 '
    htmlBody += '                                                                                                                                                                                                                                         '
    htmlBody += '<p>PLEASE DO NOT REPLY TO THIS EMAIL, IF YOU HAVE ANY QUESTIONS, ISSUES OR WOULD LIKE TO CHECK THE STATUS OF YOUR COPY JOB, please call </p>';
    textBody += '\n\nPLEASE DO NOT REPLY TO THIS EMAIL, IF YOU HAVE ANY QUESTIONS, ISSUES OR WOULD LIKE TO CHECK THE STATUS OF YOUR COPY JOB, please call \n';
    GmailApp.sendEmail(myOtherEmail + "," + myEmail, subject, textBody, { htmlBody: htmlBody,  replyTo: thierEmail});
    GmailApp.sendEmail(thierEmail, subject, textBody, { htmlBody: htmlBody,  replyTo: myOtherEmail});

}
function BackupBulkEmailSender() {
    var START = 36
    var ROWS = 1
    var myEmail = "";
    var myOtherEmail = "";
    var ss = SpreadsheetApp.getActive();
    var sheet = ss.getSheetByName('Form Responses 1');
    var e = sheet.getRange(START, 1, ROWS, sheet.getLastColumn()).getValues();
    e = e[0]
    var subject = e[3] + " " + e[2] + " - NAME - " + e[5];
    var thierEmail = e[1]
    var htmlBody = "";
    var textBody = "";

    var values = e;


    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues();
    var currentrow = sheet.getLastRow();
    var htmlBody = "<p>Your copy job has been submitted as shown below:</p><br><b>Order Number: " + ("00000" + currentrow).slice(-5) + "</b><br>";
    var textBody = "\n\n\nYour copy job has been submitted as shown below:\n\nOrder Number: " + ("00000" + currentrow).slice(-5) + "\n"

    htmlBody += '<head><style>tr:nth-child(even) {background-color: #f2f2f2;} </style> </head> <table style="border-radius:2px;margin:20px 0 25px;min-width:400px;border:1px solid #eee" cellspacing="0" cellpadding="10" border="0">';
    var rowCount = 0

    for (var i = 0; i < values.length; i++) {
        var label = headers[0][i];
        var data = values[i];
        if (rowCount % 2 == 0)
            var tr = '<tr style="background:#f9f9f9">';
        else
            var tr = '<tr>';
        if (data != "") {
            if (label.indexOf('Attach your file(s) in PDF format.') == -1) {

                htmlBody += tr + '<td style="font-weight:bold;border-bottom:1px solid #eee;width:180px"><b>' + label + '</b></td><td style="border-bottom:1px solid #eee">' + data + '</td></tr>';
                textBody += label + " " + data + "\n";
                rowCount += 1;
            }
            else {
                var filedata = "";
                var textFileData = "";
                var array = data.split(',');
                for (var j = 0; j < array.length; j++) {
                    filedata += '<a href="' + array[j] + '">File ' + (j + 1) + '</a><br>';
                    textFileData += "File " + (j + 1) + " " + array[j] + "\n"
                }
                htmlBody += tr + '<td style="font-weight:bold;border-bottom:1px solid #eee;width:180px"><b>' + label + '</b></td><td style="border-bottom:1px solid #eee">' + filedata + '</td></tr>';
                textBody += label + " " + textFileData;
                rowCount += 1;
            }
        }

    };
    htmlBody += '</table>                                                                                                                                                                                                                                 '
    htmlBody += '                                                                                                                                                                                                                                         '
    htmlBody += '<p>PLEASE DO NOT REPLY TO THIS EMAIL, IF YOU HAVE ANY QUESTIONS, ISSUES OR WOULD LIKE TO CHECK THE STATUS OF YOUR COPY JOB, please call </p>';
    textBody += '\n\nPLEASE DO NOT REPLY TO THIS EMAIL, IF YOU HAVE ANY QUESTIONS, ISSUES OR WOULD LIKE TO CHECK THE STATUS OF YOUR COPY JOB, please call \n';
    GmailApp.sendEmail(myOtherEmail + "," + myEmail, subject, textBody, { htmlBody: htmlBody,  replyTo: thierEmail});
    GmailApp.sendEmail(thierEmail, subject, textBody, { htmlBody: htmlBody,  replyTo: myOtherEmail});

}